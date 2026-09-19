import bcrypt
import os
from datetime import datetime, timedelta, timezone
import jwt

ALGORITMO = "HS256"
MINUTOS_EXPIRACION = 30

def _clave_secreta() -> str:
    clave = os.getenv("SECRET_KEY")
    if not clave:
        raise RuntimeError("Falta la variable de entorno SECRET_KEY")
    return clave

def crear_token(email: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    return jwt.encode(
        {"sub": email, "exp": expira},
        _clave_secreta(),
        algorithm=ALGORITMO,
    )

def leer_token(token: str) -> str | None:
    try:
        datos = jwt.decode(token, _clave_secreta(), algorithms=[ALGORITMO])
    except jwt.InvalidTokenError:
        return None
    return datos.get("sub")



def hashear_password(password: str) -> str:
    hash_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hash_bytes.decode()

def verificar_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())