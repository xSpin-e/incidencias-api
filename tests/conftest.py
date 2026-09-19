import pytest
from app.routers.incidentes import incidentes_db

@pytest.fixture(autouse=True)
def limpiar_db():
    incidentes_db.clear()