from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True) #Convierte de INCIDENTE_DB A INCIDENTE_DTO
    id: int

class UsuarioCrear(BaseModel):
    email: str
    password: str

class Usuario(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str