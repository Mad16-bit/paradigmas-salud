from fastapi import APIRouter
from app.schemas.health_models import PerfilSalud, RegistroProgreso
from app.infrastructure.prolog_engine import (
    obtener_recomendaciones_desde_prolog,
    guardar_progreso,
    listar_progreso,
)

router = APIRouter()


@router.get("/")
def root():
    return {"message": "API funcionando correctamente"}


@router.post("/recommendations")
def obtener_recomendaciones(perfil: PerfilSalud):
    return obtener_recomendaciones_desde_prolog(perfil)


@router.post("/progress")
def registrar_progreso(registro: RegistroProgreso):
    return guardar_progreso(registro)


@router.get("/progress")
def obtener_progreso():
    return listar_progreso()