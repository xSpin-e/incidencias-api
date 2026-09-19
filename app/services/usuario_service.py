from sqlalchemy.orm import Session
import os

from app.enum import Rol
from app.models import UsuarioDB
from app.repositories import usuario_repository
from app.schemas import Usuario, UsuarioCrear
from app.security import hashear_password, verificar_password


class EmailYaRegistrado(Exception):
    pass


def registrar_usuario(db: Session, datos: UsuarioCrear) -> Usuario:
    if usuario_repository.obtener_por_email(db, datos.email) is not None:
        raise EmailYaRegistrado()

    fila = UsuarioDB(
        email=datos.email,
        password_hash=hashear_password(datos.password),
    )
    guardado = usuario_repository.guardar(db, fila)
    return Usuario.model_validate(guardado)

class CredencialesInvalidas(Exception):
    pass

def autenticar_usuario(db: Session, email: str, password: str) -> Usuario:
    usuario = usuario_repository.obtener_por_email(db, email)
    if usuario is None or not verificar_password(password, usuario.password_hash):
        raise CredencialesInvalidas()
    return Usuario.model_validate(usuario)

def crear_admin_inicial(db: Session) -> None:
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    if not email or not password:
        return
    if usuario_repository.obtener_por_email(db, email) is not None:
        return
    admin = UsuarioDB(
        email=email,
        password_hash=hashear_password(password),
        rol=Rol.admin,
    )
    usuario_repository.guardar(db, admin)