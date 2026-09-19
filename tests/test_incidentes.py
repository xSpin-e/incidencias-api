from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    respuesta = client.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"status":"ok"}

def test_crear_incidente():
    datos = {
        "titulo": "Phising",
        "descripcion": "Correo sospechoso",
        "severidad": "media"
    }

    respuesta = client.post("/incidentes", json=datos)

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["titulo"] == "Phising"
    assert cuerpo["descripcion"] == "Correo sospechoso"
    assert cuerpo["severidad"] == "media"
    assert cuerpo["cve_id"] is None

def test_obtener_incidente():
    datos = {
        "titulo": "Phising",
        "descripcion": "Correo sospechoso",
        "severidad": "media"
    }

    respuesta_post = client.post("/incidentes", json=datos)

    assert respuesta_post.status_code == 201

    respuesta_get = client.get(f"/incidentes/{respuesta_post.json()['id']}")

    assert respuesta_get.status_code == 200
    cuerpo = respuesta_get.json()
    assert cuerpo["id"] == 1
    assert cuerpo["titulo"] == "Phising"
    assert cuerpo["descripcion"] == "Correo sospechoso"
    assert cuerpo["severidad"] == "media"
    assert cuerpo["cve_id"] is None

def test_obtener_incidente_inexistente():
    respuesta_get = client.get(f"/incidentes/100")
    assert respuesta_get.status_code == 404
    assert respuesta_get.json() == {"detail": "Incidente no encontrado"}

def test_listar_incidentes():

    datos = {
        "titulo": "Phising",
        "descripcion": "Correo sospechoso",
        "severidad": "media"
    }

    client.post("/incidentes", json=datos)

    datos2 = {
        "titulo": "Fuerza bruta",
        "descripcion": "500 intentos de login",
        "severidad": "alta"
    }
    
    client.post("/incidentes", json=datos2)

    respuesta_get = client.get("/incidentes")

    assert respuesta_get.status_code == 200
    cuerpo = respuesta_get.json()
    assert len(cuerpo) == 2

