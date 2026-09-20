# API de incidentes de seguridad

API REST para registrar incidentes de seguridad. La hice para practicar Python y para tener un proyecto completo que enseñar: desde el código hasta el despliegue en AWS.

![CI](https://github.com/xSpin-e/incidencias-api/actions/workflows/ci.yml/badge.svg)

## Qué hace

Un usuario se registra, inicia sesión y crea incidentes (por ejemplo, un correo de phishing o un intento de fuerza bruta). Solo el administrador puede listarlos y consultarlos.

## Tecnologías

Python 3.12, FastAPI, SQLAlchemy 2.0, SQLite, JWT, bcrypt, pytest, Docker, GitHub Actions y AWS (EC2).

## Cómo arrancarlo

Necesitas Docker. Copia el fichero de ejemplo de variables y rellénalo:

```bash
cp .env.example .env
docker compose up --build
```

La API queda en `http://localhost:8000` y la documentación interactiva en `http://localhost:8000/docs`.

### Variables de entorno

| Variable | Para qué sirve |
|---|---|
| `SECRET_KEY` | Clave con la que se firman los tokens. Que sea larga y alea
| `ADMIN_EMAIL` | Email del administrador que se crea al arrancar. |
| `ADMIN_PASSWORD` | Contraseña de ese administrador. |

Si falta alguna, el contenedor no arranca. El fichero `.env` no se sube al r

## Cómo usarla

Todos los ejemplos parten de `http://localhost:8000`.

**1. Registrarse** (siempre crea un usuario normal):

```bash
curl -X POST http://localhost:8000/auth/registro \
  -H "Content-Type: application/json" \
  -d '{"email": "yo@ejemplo.com", "password": "una-clave"}'
```

**2. Iniciar sesión.** Ojo: aquí no se manda JSON sino un formulario, y el e`:
```bashcurl -X POST http://localhost:8000/auth/login \  -d "username=yo@ejemplo.com&password=una-clave"```
Devuelve `{"access_token": "...", "token_type": "bearer"}`. El token caduca a los 30 minutos.                                                                                       
**3. Crear un incidente**, enviando el token en la cabecera:

```bash                                                                                                                                                                             curl -X POST http://localhost:8000/incidentes \  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \                                                                                                                                               -d '{"titulo": "Phishing", "descripcion": "Correo sospechoso", "severidad"```
## Endpoints
                                                                                                                                                                                    | Método | Ruta | Quién puede |
|---|---|---|
| GET | `/health` | Cualquiera |                                                                                                                                                    | POST | `/auth/registro` | Cualquiera |
| POST | `/auth/login` | Cualquiera |                                                                                                                                               | POST | `/incidentes` | Usuario autenticado |
| GET | `/incidentes` | Solo administrador |                                                                                                                                        | GET | `/incidentes/{id}` | Solo administrador |
                                                                                                                                                                                    Campos de un incidente: `titulo`, `descripcion` y `severidad` son obligatoriierto`) y `cve_id` son opcionales.- `severidad`: `baja`, `media`, `alta` o `critica`- `estado`: `abierto`, `en_curso` o `cerrado`Errores habituales: `401` sin token o token caducado, `403` si el usuario nol incidente no existe, `409` si el email ya está registrado y `422` si losdatos no son válidos.                                                                                                                                                               
## Tests                                                                                                                                                                            ```bashpip install -r requirements.txtpytest```

Los tests usan una base de datos en memoria, así que no tocan los datos reales.                                                                                                     
## Cómo está organizado
                                                                                                                                                                                    El código sigue cuatro capas: router, servicio, repositorio y base de datos.ntic) están separados de las tablas (SQLAlchemy).
                                                                                                                                                                                    ```
app/                                                                                                                                                                                ├── routers/        endpoints HTTP
├── services/       lógica                                                                                                                                                          ├── repositories/   consultas a la base de datos├── models.py       tablas├── schemas.py      datos que entran y salen├── security.py     hash de contraseñas y tokens└── dependencies.py comprobación de token y de rol
```                                                                                                                                                                                 
## Despliegue                                                                                                                                                                       Cuando se fusiona un cambio en `main`, GitHub Actions ejecuta los tests, conla sube a GitHub Container Registry. El servidor, una instancia EC2, tieneWatchtower, que revisa cada minuto si hay una imagen nueva y reinicia la API

La demo en AWS es temporal y puede no estar disponible.
