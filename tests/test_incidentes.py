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

def test_registro(client):
    respuesta = client.post("/auth/registro", json={"email": "a@a.com", "password": "1234"})
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["email"] == "a@a.com"
    assert cuerpo["rol"] == "usuario"
    assert "password" not in cuerpo
    assert "password_hash" not in cuerpo


def test_registro_email_repetido(client):
    datos = {"email": "a@a.com", "password": "1234"}
    client.post("/auth/registro", json=datos)
    respuesta = client.post("/auth/registro", json=datos)
    assert respuesta.status_code == 409

def test_login_correcto(client):
    client.post("/auth/registro", json={"email": "a@a.com", "password": "1234"})
    respuesta = client.post(
        "/auth/login", data={"username": "a@a.com", "password": "1234"}
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["token_type"] == "bearer"
    assert "access_token" in respuesta.json()


def test_login_password_incorrecta(client):
    client.post("/auth/registro", json={"email": "a@a.com", "password": "1234"})
    respuesta = client.post(
        "/auth/login", data={"username": "a@a.com", "password": "mala"}
    )
    assert respuesta.status_code == 401

DATOS = {"titulo": "Phishing", "descripcion": "Correo sospechoso", "severidad": "media"}

def test_crear_incidente_sin_token(client):
    assert client.post("/incidentes", json=DATOS).status_code == 401


def test_listar_sin_token(client):
    assert client.get("/incidentes").status_code == 401


def test_listar_como_usuario_prohibido(client, token_usuario):
    assert client.get("/incidentes", headers=token_usuario).status_code == 403


def test_obtener_como_usuario_prohibido(client, token_usuario):
    assert client.get("/incidentes/1", headers=token_usuario).status_code == 403


def test_token_falso(client):
    respuesta = client.get("/incidentes", headers={"Authorization": "Bearer falso"})
    assert respuesta.status_code == 401