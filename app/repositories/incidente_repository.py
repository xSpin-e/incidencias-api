from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import IncidenteDB


def guardar(db: Session, incidente: IncidenteDB) -> IncidenteDB:
    db.add(incidente)
    db.commit()
    db.refresh(incidente) #Actualiza los datos de incidente en la base de datos
    return incidente

def listar(db: Session) -> list[IncidenteDB]:
    consulta = select(IncidenteDB)      # 1. escribo la pregunta
    resultado = db.scalars(consulta)    # 2. se la hago a la base de datos
    filas = resultado.all()             # 3. recojo todas las respuestas
    return list(filas)      # 4. las devuelvo en una lista