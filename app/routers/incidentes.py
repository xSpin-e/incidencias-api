from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.database import DbSession
from app.dependencies import solo_admin, usuario_actual
from app.schemas import Incidente, IncidenteCrear, Usuario
from app.services import incidente_service



router = APIRouter(prefix="/incidentes", tags=["incidentes"])

@router.post("", response_model=Incidente, status_code=201)
def crear_incidente(datos: IncidenteCrear, db: DbSession, usuario: Annotated[Usuario, Depends(usuario_actual)]): #ejecuta primero la funcion y deja el resultado en usuario
    return incidente_service.crear_incidente(db, datos)

@router.get("", response_model=list[Incidente], dependencies=[Depends(solo_admin)])
def obtener_incidentes(db: DbSession):
    return incidente_service.listar_incidentes(db)

@router.get("/{incidente_id}", response_model=Incidente, dependencies=[Depends(solo_admin)])
def obtener_incidente(db: DbSession, incidente_id: int):
    incidente = incidente_service.obtener_por_id(db, incidente_id)
    if incidente is None:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    return incidente
