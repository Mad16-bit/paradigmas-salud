from fastapi import APIRouter
from app.schemas.health_models import PerfilSalud
from app.infrastructure.prolog_engine import obtener_recomendaciones_desde_prolog

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "API funcionando correctamente",
        "endpoints": [
            {"method": "GET", "path": "/", "description": "Estado general de la API"},
            {"method": "POST", "path": "/recommendations", "description": "Genera recomendaciones de salud"},
            {"method": "POST", "path": "/users", "description": "Crea un usuario"},
            {"method": "POST", "path": "/profiles", "description": "Crea un perfil de salud para un usuario"},
            {"method": "GET", "path": "/profiles/{user_id}", "description": "Obtiene el perfil más reciente de un usuario"},
            {"method": "GET", "path": "/profiles/{user_id}/history", "description": "Obtiene el historial de perfiles de un usuario"},
            {"method": "GET", "path": "/recommendations/{user_id}", "description": "Genera recomendaciones para el perfil más reciente de un usuario"},
            {"method": "POST", "path": "/progress", "description": "Registra progreso semanal de un usuario"},
            {"method": "GET", "path": "/progress/{user_id}", "description": "Lista el progreso registrado de un usuario"},
        ],
    }


@router.post("/recommendations")
def obtener_recomendaciones(perfil: PerfilSalud):
    return obtener_recomendaciones_desde_prolog(perfil)
