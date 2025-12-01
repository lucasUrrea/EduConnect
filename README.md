# EduConnect — Instrucciones de desarrollo

Este README contiene instrucciones para ejecutar y probar localmente el proyecto EduConnect (Django). Está pensado para desarrollo en Windows con PowerShell.

Resumen rápido
- Proyecto: Django 5.2.x
- Base de datos por defecto en desarrollo: SQLite (activar con variable de entorno USE_SQLITE=1)
- MariaDB/MySQL: soportado (usamos PyMySQL en Windows)
- API REST: Django REST Framework + token auth
- Documentación API: Swagger UI en `/api/docs/`

Requisitos
- Python 3.11+ (en este entorno se usó Python 3.13)
- Git (opcional)
- Microsoft Visual C++ Build Tools solo si quieres instalar `mysqlclient` en Windows (no necesario si usas PyMySQL)

Archivos importantes
- `manage.py` — script de administración Django
- `modulos_consultas/settings.py` — configuración principal (usa USE_SQLITE=1 para SQLite)
- `EduConnectApp/` — app principal (modelos, vistas, templates, APIs)
- `requirements.txt` — dependencias del proyecto
- `scripts/` — scripts útiles: `create_test_users.py`, `seed_example_data.py`, `test_api_calls.py`

Credenciales de ejemplo (solo para entorno de desarrollo)
- Superuser admin (creado por script):
  - Usuario: `admin@example.com`
  - Contraseña: `AdminPass123!`
- Usuario estudiante (creado por script):
  - Usuario: `teststudent@example.com`
  - Contraseña: `TestPass123!`
- Usuario semilla adicional:
  - `student1@example.com` / `StudPass123!`
  - `docente1@example.com` / `DocPass123!`

Cómo ejecutar localmente (PowerShell)

1) Crear y activar un entorno virtual

```powershell
# desde la raíz del proyecto (donde está manage.py)
python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
. .\.venv\Scripts\Activate.ps1
```

2) Instalar dependencias

```powershell
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
```

3) Usar SQLite (recomendado para desarrollo rápido)

```powershell
$env:USE_SQLITE='1'
.\.venv\Scripts\python .\manage.py makemigrations
.\.venv\Scripts\python .\manage.py migrate
```

Si prefieres MariaDB/MySQL, edita `modulos_consultas/settings.py` para actualizar `DATABASES` (user, password, name, host) o usa variables de entorno y luego ejecuta `migrate` sin `USE_SQLITE=1`.

Notas sobre MySQL/MariaDB en Windows
- Este proyecto usa `pymysql` (pure-Python) para evitar necesidad de compilar `mysqlclient` en Windows.
- Si usas `mysqlclient`, instala Visual C++ Build Tools y las librerías MySQL necesarias.
- Si tu servidor MariaDB usa `caching_sha2_password`, confirma que tu driver lo soporta; de lo contrario crea un usuario con `mysql_native_password`.

4) Crear usuarios de prueba y poblar datos de ejemplo (opcional)

```powershell
# crear superuser y usuario de prueba
.\.venv\Scripts\python .\manage.py shell -c "exec(open('scripts/create_test_users.py').read())"

# poblar datos de ejemplo (asignaturas, categorias, docente, estudiante, consulta, respuesta)
.\.venv\Scripts\python .\manage.py shell -c "exec(open('scripts/seed_example_data.py', encoding='utf-8').read())"
```

5) Ejecutar el servidor de desarrollo

```powershell
$env:USE_SQLITE='1'  # si quieres usar SQLite
.\.venv\Scripts\python .\manage.py runserver
```
Abre http://127.0.0.1:8000/ y http://127.0.0.1:8000/admin/ (usa el superuser).

API REST

- Endpoints disponibles (ejemplos):
  - GET/POST/PUT/DELETE `/api/consultas/`
  - GET/POST/PUT/DELETE `/api/respuestas/`
  - GET `/api/usuarios/`
  - GET/POST `/api/asignaturas/`
  - GET/POST `/api/categorias/`
  - GET/POST `/api/docentes/`

- Obtener token (DRF Token Auth):
  - `POST /api-token-auth/` con JSON `{"username": "user@example.com", "password": "pass"}`
  - Respuesta: `{"token": "<token>"}`

- Ejemplo curl autenticado (reemplaza `<token>`):

```bash
curl -H "Authorization: Token <token>" http://127.0.0.1:8000/api/consultas/
```

Documentación OpenAPI / Swagger
- Esquema: `/api/schema/`
- Swagger UI: `/api/docs/`

Tokens de prueba
- Los tokens para los usuarios de prueba fueron creados automáticamente por un script de tests. Para obtener tu propio token usa `/api-token-auth/`.

Pruebas (tests)

```powershell
$env:USE_SQLITE='1'
.\.venv\Scripts\python .\manage.py test -v 2
```

Notas de seguridad y producción
- No expongas `SECRET_KEY` ni credenciales en repositorios públicos.
- Para producción configura `ALLOWED_HOSTS`, HTTPS/TLS y un servidor WSGI/ASGI (Gunicorn, uWSGI, Daphne, etc.).
- Usa almacenamiento seguro para `MEDIA_ROOT` (S3, GCS) si necesitas subir archivos en producción.
- Revisa y migra a un modelo de usuario consolidado (`AUTH_USER_MODEL`) si planeas usar Django auth plenamente. El repo actualmente mantiene la tabla `Usuarios` y sincroniza con `auth.User` para compatibilidad (opción B).

Problemas comunes y soluciones rápidas
- Error al crear venv en OneDrive: crea el venv fuera de la carpeta sincronizada o desactiva temporalmente la sincronización.
- Error `ModuleNotFoundError: No module named 'modulos_consultas'` al ejecutar scripts: ejecuta el script desde `manage.py shell` o asegúrate de estar en la raíz del proyecto.
- Error instalando `mysqlclient` en Windows: usa `pymysql` o instala Build Tools.

Contacto / Siguientes pasos
- Puedo añadir autenticación JWT (SimpleJWT), endpoints adicionales, mejorar permisos y roles, o convertir `Usuarios` a `CustomUser` (operación más invasiva). Dime qué prefieres y lo implemento.

---

Archivo generado automáticamente por las herramientas de desarrollo el 09-10-2025.
