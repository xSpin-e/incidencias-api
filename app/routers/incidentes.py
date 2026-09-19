from fastapi import APIRouter, HTTPException
from app.schemas import Incidente, IncidenteCrear
from app.services import incidente_service
from app.database import DbSession

router = APIRouter(prefix="/incidentes", tags=["incidentes"])
incidentes_db: dict[int, Incidente] = {}

@router.post("", response_model=Incidente, status_code=201)
def crear_incidente(datos: IncidenteCrear, db: DbSession):
    return incidente_service.crear_incidente(db, datos)

@router.get("", response_model=list[Incidente])
def obtener_incidentes(db: DbSession):
    return incidente_service.listar_incidentes(db)

@router.get("/{incidente_id}", response_model=Incidente)
def obtener_incidente(incidente_id: int):
    if incidente_id not in incidentes_db:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    return incidentes_db[incidente_id]