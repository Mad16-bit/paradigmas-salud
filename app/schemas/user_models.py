from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class NivelActividadEnum(str, Enum):
    sedentario = "sedentario"
    levemente_activo = "levemente_activo"
    moderadamente_activo = "moderadamente_activo"
    # muy_activo: salud_rules.pl todavia no tiene ejercicio_recomendado/3
    # para este nivel, asi que /recommendations puede devolver
    # "ejercicio": [] hasta que se actualice la base de Prolog.
    muy_activo = "muy_activo"


class ObjetivoEnum(str, Enum):
    perdida_peso = "perdida_peso"
    ganancia_muscular = "ganancia_muscular"
    mantenimiento = "mantenimiento"
    mejora_cardiovascular = "mejora_cardiovascular"
    reduccion_estres = "reduccion_estres"


class NivelEstresEnum(str, Enum):
    alto_estres = "alto_estres"
    pocas_horas_sueno = "pocas_horas_sueno"
    sedentario = "sedentario"


class UsuarioCreate(BaseModel):
    nombre: str
    correo: str


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    correo: str
    creado_en: datetime


class PerfilCreate(BaseModel):
    usuario_id: int
    nivel_actividad: NivelActividadEnum
    objetivo: ObjetivoEnum
    nivel_estres: NivelEstresEnum | None = None
    alergias: str | None = None
    condiciones: list[str]


class PerfilResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    nivel_actividad: str
    objetivo: str
    nivel_estres: str | None
    alergias: str | None
    fecha_registro: datetime
    condiciones: list[str]


class ProgresoCreate(BaseModel):
    usuario_id: int
    peso: float
    horas_sueno: float
    actividad_realizada: str


class ProgresoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    peso: float
    horas_sueno: float
    actividad_realizada: str
    fecha_registro: datetime
