from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from app.database import DbSession
from app.enum import Rol
from app.schemas import Usuario
from app.security import leer_token
from app.services import usuario_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def usuario_actual(
    request: Request,
    token_cabecera: Annotated[str | None, Depends(oauth2_scheme)],
    db: DbSession,) -> Usuario:
    token = token_cabecera or request.cookies.get("access_token")
    email = leer_token(token) if token else None
    usuario = usuario_service.obtener_usuario_por_email(db, email) if email else None
    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o caducado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return usuario


def solo_admin(usuario: Annotated[Usuario, Depends(usuario_actual)]) -> Usuario:
    if usuario.rol != Rol.admin:
        raise HTTPException(status_code=403, detail="Se requiere rol de admin")
    return usuario