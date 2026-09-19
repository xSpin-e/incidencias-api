from fastapi import APIRouter, HTTPException
from app.database import DbSession
from app.schemas import Usuario, UsuarioCrear
from app.services import usuario_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registro", response_model=Usuario, status_code=201)
def registro(datos: UsuarioCrear, db: DbSession):
    try:
        return usuario_service.registrar_usuario(db, datos)
    except usuario_service.EmailYaRegistrado:
        raise HTTPException(status_code=409, detail="El email ya está registrado")