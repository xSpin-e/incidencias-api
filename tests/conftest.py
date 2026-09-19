import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401
from app.database import Base, get_db
from app.main import app
from app.services import usuario_service


@pytest.fixture(autouse=True)
def variables_entorno(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "clave-de-tests-" + "x" * 32)
    monkeypatch.setenv("ADMIN_EMAIL", "admin@test.com")
    monkeypatch.setenv("ADMIN_PASSWORD", "admin1234")


@pytest.fixture
def client(variables_entorno):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(bind=engine, autoflush=False)

    with testing_session() as db:
        usuario_service.crear_admin_inicial(db)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def token_usuario(client):
    datos = {"email": "user@test.com", "password": "user1234"}
    client.post("/auth/registro", json=datos)
    respuesta = client.post(
        "/auth/login",
        data={"username": datos["email"], "password": datos["password"]},
    )
    return {"Authorization": f"Bearer {respuesta.json()['access_token']}"}


@pytest.fixture
def token_admin(client):
    respuesta = client.post(
        "/auth/login",
        data={"username": "admin@test.com", "password": "admin1234"},
    )
    return {"Authorization": f"Bearer {respuesta.json()['access_token']}"}