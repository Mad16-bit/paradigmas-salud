from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.health_routes import router as health_router
from app.api.routes.user_routes import router as user_router
from app.infrastructure.db import Base, engine, SessionLocal
from app.models.db_models import seed_condiciones

app = FastAPI(title="Paradigmas Salud API")

app.add_middleware(
	CORSMiddleware,
	allow_origins=[
		"http://localhost:3000",
		"http://127.0.0.1:3000",
		"http://localhost:5173",
		"http://127.0.0.1:5173",
	],
	allow_credentials=False,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
	Base.metadata.create_all(bind=engine)
	db = SessionLocal()
	try:
		seed_condiciones(db)
	finally:
		db.close()


app.include_router(health_router)
app.include_router(user_router)
