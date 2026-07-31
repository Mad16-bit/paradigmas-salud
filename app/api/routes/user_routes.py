from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.db import get_db
from app.infrastructure.prolog_engine import obtener_recomendaciones_desde_prolog
from app.infrastructure.security import hash_password, verify_password
from app.models.db_models import Condicion, PerfilSaludDB, ProgresoSemanal, Usuario
from app.schemas.health_models import PerfilSalud
from app.schemas.user_models import (
    LoginRequest,
    PerfilCreate,
    PerfilResponse,
    ProgresoCreate,
    ProgresoResponse,
    UsuarioCreate,
    UsuarioResponse,
)

router = APIRouter()


def _get_usuario_or_404(db: Session, usuario_id: int) -> Usuario:
    usuario = db.get(Usuario, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail=f"Usuario {usuario_id} no encontrado")
    return usuario


def _to_perfil_response(perfil: PerfilSaludDB) -> PerfilResponse:
    return PerfilResponse(
        id=perfil.id,
        usuario_id=perfil.usuario_id,
        nivel_actividad=perfil.nivel_actividad,
        objetivo=perfil.objetivo,
        nivel_estres=perfil.nivel_estres,
        alergias=perfil.alergias,
        fecha_registro=perfil.fecha_registro,
        condiciones=[c.codigo for c in perfil.condiciones],
    )


@router.post("/users", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(payload: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.correo == payload.correo).first()
    if existente is not None:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo")
    usuario = Usuario(
        nombre=payload.nombre,
        correo=payload.correo,
        password_hash=hash_password(payload.password),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=UsuarioResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.correo == payload.correo).first()
    if usuario is None or not verify_password(payload.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return usuario


@router.post("/profiles", response_model=PerfilResponse, status_code=status.HTTP_201_CREATED)
def crear_perfil(payload: PerfilCreate, db: Session = Depends(get_db)):
    _get_usuario_or_404(db, payload.usuario_id)

    condiciones_db = []
    codigos_invalidos = []
    for codigo in payload.condiciones:
        condicion = db.query(Condicion).filter(Condicion.codigo == codigo).first()
        if condicion is None:
            codigos_invalidos.append(codigo)
        else:
            condiciones_db.append(condicion)

    if codigos_invalidos:
        raise HTTPException(
            status_code=400,
            detail=f"Códigos de condición no reconocidos: {', '.join(codigos_invalidos)}",
        )

    perfil = PerfilSaludDB(
        usuario_id=payload.usuario_id,
        nivel_actividad=payload.nivel_actividad.value,
        objetivo=payload.objetivo.value,
        nivel_estres=payload.nivel_estres.value if payload.nivel_estres else None,
        alergias=payload.alergias,
        condiciones=condiciones_db,
    )
    db.add(perfil)
    db.commit()
    db.refresh(perfil)
    return _to_perfil_response(perfil)


@router.get("/profiles/{user_id}", response_model=PerfilResponse)
def obtener_perfil_actual(user_id: int, db: Session = Depends(get_db)):
    _get_usuario_or_404(db, user_id)
    perfil = (
        db.query(PerfilSaludDB)
        .filter(PerfilSaludDB.usuario_id == user_id)
        .order_by(PerfilSaludDB.fecha_registro.desc())
        .first()
    )
    if perfil is None:
        raise HTTPException(status_code=404, detail="El usuario no tiene perfiles registrados")
    return _to_perfil_response(perfil)


@router.get("/profiles/{user_id}/history", response_model=list[PerfilResponse])
def obtener_historial_perfiles(user_id: int, db: Session = Depends(get_db)):
    _get_usuario_or_404(db, user_id)
    perfiles = (
        db.query(PerfilSaludDB)
        .filter(PerfilSaludDB.usuario_id == user_id)
        .order_by(PerfilSaludDB.fecha_registro.desc())
        .all()
    )
    return [_to_perfil_response(p) for p in perfiles]


@router.get("/recommendations/{user_id}")
def obtener_recomendaciones_usuario(user_id: int, db: Session = Depends(get_db)):
    _get_usuario_or_404(db, user_id)
    perfil = (
        db.query(PerfilSaludDB)
        .filter(PerfilSaludDB.usuario_id == user_id)
        .order_by(PerfilSaludDB.fecha_registro.desc())
        .first()
    )
    if perfil is None:
        raise HTTPException(status_code=404, detail="El usuario no tiene perfiles registrados")

    perfil_pydantic = PerfilSalud(
        condiciones=[c.codigo for c in perfil.condiciones],
        nivel_actividad=perfil.nivel_actividad,
        objetivo=perfil.objetivo,
        nivel_estres=perfil.nivel_estres,
    )
    return obtener_recomendaciones_desde_prolog(perfil_pydantic)


@router.post("/progress", response_model=ProgresoResponse, status_code=status.HTTP_201_CREATED)
def registrar_progreso(payload: ProgresoCreate, db: Session = Depends(get_db)):
    _get_usuario_or_404(db, payload.usuario_id)
    registro = ProgresoSemanal(
        usuario_id=payload.usuario_id,
        peso=payload.peso,
        horas_sueno=payload.horas_sueno,
        actividad_realizada=payload.actividad_realizada,
    )
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return registro


@router.get("/progress/{user_id}", response_model=list[ProgresoResponse])
def obtener_progreso_usuario(user_id: int, db: Session = Depends(get_db)):
    _get_usuario_or_404(db, user_id)
    registros = (
        db.query(ProgresoSemanal)
        .filter(ProgresoSemanal.usuario_id == user_id)
        .order_by(ProgresoSemanal.fecha_registro.desc())
        .all()
    )
    return registros
