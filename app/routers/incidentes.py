from fastapi import APIRouter, HTTPException
from app.schemas import Incidente, IncidenteCrear

router = APIRouter(prefix="/incidentes", tags=["incidentes"])
incidentes_db: dict[int, Incidente] = {}

@router.post("", response_model=Incidente, status_code=201)
def crear_incidente(datos: IncidenteCrear):
    nuevo_id = len(incidentes_db) + 1
    incidente = Incidente(id=nuevo_id, **datos.model_dump()) #convierte la información en un diccionario
    incidentes_db[nuevo_id] = incidente
    return incidente

@router.get("", response_model=list[Incidente])
def obtener_incidentes():
    return list(incidentes_db.values())

@router.get("/{incidente_id}", response_model=Incidente)
def obtener_incidente(incidente_id: int):
    if incidente_id not in incidentes_db:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    return incidentes_db[incidente_id]