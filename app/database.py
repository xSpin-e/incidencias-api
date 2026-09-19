import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./incidentes.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

def get_db():
    db = SessionLocal()      # 1. abrir
    try:
        yield db             # 2. prestar
    finally:
        db.close()           # 3. cerrar

class Base(DeclarativeBase):
    pass