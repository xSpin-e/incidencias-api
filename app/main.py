from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import incidentes
from app.routers import usuarios
from app.database import SessionLocal, init_db
from app.services import usuario_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    with SessionLocal() as db:
        usuario_service.crear_admin_inicial(db)
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://scorpion.adrianespin.com",
        "http://localhost:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(incidentes.router)
app.include_router(usuarios.router)

@app.get("/health")
def health():
    return{"status": "maintenance"}






