from sqlalchemy.orm import Session

from app.models import IncidenteDB
from app.repositories import incidente_repository
from app.schemas import Incidente, IncidenteCrear


def crear_incidente(db: Session, datos: IncidenteCrear) -> Incidente:
    fila = IncidenteDB(**datos.model_dump())
    guardada = incidente_repository.guardar(db, fila)
    return Incidente.model_validate(guardada)

def listar_incidentes(db: Session) -> list[Incidente]:
    filas = incidente_repository.listar(db)
    return [Incidente.model_validate(fila) for fila in filas]

def obtener_por_id(db: Session, incidente_id: int) -> Incidente | None:
    fila = incidente_repository.obtener_por_id(db, incidente_id)
    if fila is None:
        return None
    return Incidente.model_validate(fila) #El validate convierte de DB a DTO