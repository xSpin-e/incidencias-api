from pydantic import BaseModel
from app.enum import Estado
from app.enum import Severidad


# Lo que recibe la API
class IncidenteCrear(BaseModel):
    titulo: str
    descripcion: str
    severidad: Severidad
    estado: Estado = Estado.abierto
    cve_id: str | None = None

# Lo que devuelve la API
class Incidente(IncidenteCrear):
    id: int