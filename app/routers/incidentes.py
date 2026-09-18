from fastapi import APIRouter
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