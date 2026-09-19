from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import UsuarioDB

def guardar(db: Session, usuario: UsuarioDB) -> UsuarioDB:
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def obtener_por_email(db: Session, email: str) -> UsuarioDB | None:
    return db.scalars(select(UsuarioDB).where(UsuarioDB.email == email)).first()
