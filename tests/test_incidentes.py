def test_health(client):
    respuesta = client.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"status":"ok"}

def test_crear_incidente(client, token_usuario): #ejecuta  primero la función client y en el código usamos lo que devuelve
    datos = {
        "titulo": "Phising",
        "descripcion": "Correo sospechoso",
        "severidad": "media"
    }

    respuesta = client.post("/incidentes", json=datos, headers=token_usuario)

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["titulo"] == "Phising"
    assert cuerpo["descripcion"] == "Correo sospechoso"
    assert cuerpo["severidad"] == "media"
    assert cuerpo["cve_id"] is None

def test_obtener_incidente(client, token_usuario, token_admin):
    datos = {
        "titulo": "Phising",
        "descripcion": "Correo sospechoso",
        "severidad": "media"
    }

    respuesta_post = client.post("/incidentes", json=datos, headers=token_usuario)

    assert respuesta_post.status_code == 201

    respuesta_get = client.get(f"/incidentes/{respuesta_post.json()['id']}", headers=token_admin)

    assert respuesta_get.status_code == 200
    cuerpo = respuesta_get.json()
    assert cuerpo["id"] == 1
    assert cuerpo["titulo"] == "Phising"
    assert cuerpo["descripcion"] == "Correo sospechoso"
    assert cuerpo["severidad"] == "media"
    assert cuerpo["cve_id"] is None

def test_obtener_incidente_inexistente(client, token_admin):
    respuesta_get = client.get(f"/incidentes/10032131", headers=token_admin)
    assert respuesta_get.status_code == 404
    assert respuesta_get.json() == {"detail": "Incidente no encontrado"}

def test_listar_incidentes(client, token_admin):

    datos = {
        "titulo": "Phising",
        "descripcion": "Correo sospechoso",
        "severidad": "media"
    }

    client.post("/incidentes", json=datos, headers=token_admin)

    datos2 = {
        "titulo": "Fuerza bruta",
        "descripcion": "500 intentos de login",
        "severidad": "alta"
    }

    client.post("/incidentes", json=datos2, headers=token_admin)

    respuesta_get = client.get("/incidentes", headers=token_admin)

    assert respuesta_get.status_code == 200
    cuerpo = respuesta_get.json()
    assert len(cuerpo) == 2

def test_crear_incidente_severidad_invalida(client, token_usuario):
    datos = {
        "titulo": "Phishing",
        "descripcion": "Correo sospechoso",
        "severidad": "catastrofe",
    }
    respuesta = client.post("/incidentes", json=datos, headers=token_usuario)

    assert respuesta.status_code == 422