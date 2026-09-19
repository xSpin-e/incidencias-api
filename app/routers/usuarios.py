from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.database import DbSession
from app.schemas import Usuario, UsuarioCrear
from app.security import crear_token
from app.services import usuario_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registro", response_model=Usuario, status_code=201)
def registro(datos: UsuarioCrear, db: DbSession):
    try:
        return usuario_service.registrar_usuario(db, datos)
    except usuario_service.EmailYaRegistrado:
        raise HTTPException(status_code=409, detail="El email ya está registrado")

@router.post("/login")
def login(formulario: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    try:
        usuario = usuario_service.autenticar_usuario(
            db, formulario.username, formulario.password
        )
    except usuario_service.CredencialesInvalidas:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"access_token": crear_token(usuario.email), "token_type": "bearer"}