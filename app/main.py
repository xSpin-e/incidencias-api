from fastapi import FastAPI
from fastapi import APIRouter

app = FastAPI()
router = APIRouter(prefix="/soporte")


@app.get("/health")
def health():
    return{"status": "ok"}






