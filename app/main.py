from fastapi import FastAPI
from app.routers import incidentes

app = FastAPI()
app.include_router(incidentes.router)

@app.get("/health")
def health():
    return{"status": "ok"}






