from pydantic import BaseModel


class PerfilSalud(BaseModel):
    condiciones: list[str]
    nivel_actividad: str
    objetivo: str
    nivel_estres: str | None = None


class RegistroProgreso(BaseModel):
    usuario: str
    peso: float
    horas_sueno: float
    actividad_realizada: str