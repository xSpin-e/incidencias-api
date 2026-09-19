from sqlalchemy.orm import Session

from app.models import IncidenteDB


def guardar(db: Session, incidente: IncidenteDB) -> IncidenteDB:
    db.add(incidente)
    db.commit()
    db.refresh(incidente) #Actualiza los datos de incidente en la base de datos
    return incidente