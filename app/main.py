from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import incidentes
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(incidentes.router)


@app.get("/health")
def health():
    return{"status": "ok"}






