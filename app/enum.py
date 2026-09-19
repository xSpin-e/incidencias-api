from enum import StrEnum


class Severidad(StrEnum):
    baja = "baja"
    media = "media"
    alta = "alta"
    critica = "critica"

class Estado(StrEnum):
    abierto = "abierto"
    en_curso = "en_curso"
    cerrado = "cerrado"