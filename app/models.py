from sqlalchemy.orm import Mapped, mapped_column
from app.enum import Estado
from app.database import Base

#BASE ES COMO EL @ENTITY DE JPA
class IncidenteDB(Base):
    __tablename__ = "incidentes"
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]
    descripcion: Mapped[str]
    severidad: Mapped[str]
    estado: Mapped[str] = mapped_column(default=Estado.abierto)
    cve_id: Mapped[str | None]

class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]