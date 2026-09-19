from sqlalchemy.orm import Session

from app.models import IncidenteDB
from app.repositories import incidente_repository
from app.schemas import Incidente, IncidenteCrear


def crear_incidente(db: Session, datos: IncidenteCrear) -> Incidente:
    fila = IncidenteDB(**datos.model_dump())
    guardada = incidente_repository.guardar(db, fila)
    return Incidente.model_validate(guardada)