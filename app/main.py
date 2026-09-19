from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import incidentes
from app.database import init_db
from app.routers import usuarios

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(incidentes.router)
app.include_router(usuarios.router)


@app.get("/health")
def health():
    return{"status": "ok"}






