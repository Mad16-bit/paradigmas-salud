from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, Session

from app.infrastructure.db import Base

CONDICIONES_CATALOGO = [
    "diabetes_tipo_2",
    "hipertension",
    "hipotiroidismo",
    "obesidad",
    "anemia",
    "intolerancia_lactosa",
    "celiaquia",
]

perfil_condiciones = Table(
    "perfil_condiciones",
    Base.metadata,
    Column("perfil_id", Integer, ForeignKey("perfiles_salud.id"), primary_key=True),
    Column("condicion_id", Integer, ForeignKey("condiciones.id"), primary_key=True),
)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, nullable=False, unique=True, index=True)
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    perfiles = relationship("PerfilSaludDB", back_populates="usuario")
    progresos = relationship("ProgresoSemanal", back_populates="usuario")


class Condicion(Base):
    __tablename__ = "condiciones"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, nullable=False, unique=True, index=True)

    perfiles = relationship("PerfilSaludDB", secondary=perfil_condiciones, back_populates="condiciones")


class PerfilSaludDB(Base):
    __tablename__ = "perfiles_salud"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    nivel_actividad = Column(String, nullable=False)
    objetivo = Column(String, nullable=False)
    nivel_estres = Column(String, nullable=True)
    alergias = Column(String, nullable=True)
    fecha_registro = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    usuario = relationship("Usuario", back_populates="perfiles")
    condiciones = relationship("Condicion", secondary=perfil_condiciones, back_populates="perfiles")


class ProgresoSemanal(Base):
    __tablename__ = "progreso_semanal"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    peso = Column(Float, nullable=False)
    horas_sueno = Column(Float, nullable=False)
    actividad_realizada = Column(String, nullable=False)
    fecha_registro = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    usuario = relationship("Usuario", back_populates="progresos")


def seed_condiciones(db: Session) -> None:
    existentes = {c.codigo for c in db.query(Condicion).all()}
    faltantes = [codigo for codigo in CONDICIONES_CATALOGO if codigo not in existentes]
    for codigo in faltantes:
        db.add(Condicion(codigo=codigo))
    if faltantes:
        db.commit()
