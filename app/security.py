import bcrypt

def hashear_password(password: str) -> str:
    hash_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hash_bytes.decode()

def verificar_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())