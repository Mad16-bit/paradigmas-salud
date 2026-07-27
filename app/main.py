from fastapi import FastAPI
from app.api.routes.health_routes import router

app = FastAPI(title="Paradigmas Salud API")

app.include_router(router)