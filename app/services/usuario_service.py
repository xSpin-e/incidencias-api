from sqlalchemy.orm import Session

from app.models import UsuarioDB
from app.repositories import usuario_repository
from app.schemas import Usuario, UsuarioCrear
from app.security import hashear_password


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