from enum import StrEnum
from pydantic import BaseModel

class Severidad(StrEnum):
    baja = "baja"
    media = "media"
    alta = "alta"
    critica = "critica"

class Estado(StrEnum):
    abierto = "abierto"
    en_curso = "en_curso"
    cerrado = "cerrado"

class IncidenteCrear(BaseModel):
    titulo: str
    descripcion: str
    severidad: Severidad
    estado: Estado = Estado.abierto
    cve_id: str | None = None