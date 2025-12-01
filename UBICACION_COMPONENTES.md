# 📍 UBICACIÓN DE COMPONENTES PRINCIPALES

**Proyecto:** Sistema EduConnect - Módulo de Consultas  
**Fecha:** 30/11/2025

---

## 🗂️ ESTRUCTURA GENERAL

```
modulos_consultas/                      # Carpeta principal del proyecto
├── modulos_consultas/                  # Configuración del proyecto Django
├── EduConnectApp/                      # Aplicación principal
│   ├── models.py                       # Modelos de datos
│   ├── views.py                        # Vistas web (HTML)
│   ├── urls.py                         # URLs web
│   ├── forms.py                        # Formularios
│   ├── api/
│   │   ├── views.py                    # ViewSets API REST
│   │   ├── serializers.py              # Serializers JSON
│   │   └── urls.py                     # URLs API
│   ├── templates/                      # Templates HTML
│   └── static/                         # CSS, JS, imágenes
├── requirements.txt                    # Dependencias Python
├── manage.py                           # Gestión Django
└── db.sqlite3                          # Base de datos (desarrollo)
```

---

## 🔐 1. CONTROL DE USUARIOS

### 📍 Ubicación Principal

**Archivo:** `EduConnectApp/models.py` (líneas 160-200)

```python
class Usuarios(models.Model):
    """Modelo principal de usuarios - Base para estudiantes y docentes"""
    id_usuario = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=100)
    password_hash = models.CharField(max_length=255)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True)
    tipo_usuario = models.CharField(max_length=10)  # 'estudiante', 'docente', 'admin'
    # ... más campos
```

### 🔑 Características Implementadas

| Característica | Ubicación | Detalles |
|---|---|---|
| **Modelo de Usuarios** | `EduConnectApp/models.py:160` | 14 campos, tipos: estudiante, docente, admin |
| **Modelo Estudiantes** | `EduConnectApp/models.py:195` | OneToOne → Usuarios |
| **Modelo Docentes** | `EduConnectApp/models.py:215` | OneToOne → Usuarios |
| **Sistema de Autenticación** | `EduConnectApp/views.py:200` | Función `login_view()` |
| **Validación de Passwords** | `modulos_consultas/settings.py:180` | `AUTH_PASSWORD_VALIDATORS` |
| **Permisos por Rol** | `EduConnectApp/decorators.py` | 3 decoradores: `@student_only`, `@teacher_only`, `@admin_only` |
| **Sesiones** | `modulos_consultas/settings.py:95` | Configuración SESSION_COOKIE_* |
| **Token Authentication** | `modulos_consultas/settings.py:246` | Token API para acceso programático |

### 🔗 Endpoints de Usuarios

```
GET    /api/usuarios/               → Listar usuarios
GET    /api/usuarios/{id}/          → Detalle usuario
POST   /login/                       → Autenticación web
POST   /logout/                      → Cierre de sesión
POST   /api-token-auth/              → Token API
```

### 📝 Scripts de Gestión

```
verificar_y_crear_admin.py            → Crear/verificar admin
listar_cuentas.py                     → Listar usuarios
reparar_cuentas.py                    → Reparar usuarios
reset_admin_password.py               → Resetear password
```

---

## 🗄️ 2. CONEXIÓN A BASE DE DATOS MySQL/MariaDB

### 📍 Ubicación de Configuración

**Archivo:** `modulos_consultas/settings.py` (líneas 120-155)

```python
# Base de datos - Multi-BD (SQLite para desarrollo, MySQL para producción)
if os.getenv('USE_SQLITE', 'false').lower() == 'true':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Producción: MySQL/MariaDB
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'bdxd'),
            'USER': os.getenv('DB_USER', 'root'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'admin'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            }
        }
    }
```

### 🔧 Componentes de Base de Datos

| Componente | Ubicación | Detalles |
|---|---|---|
| **Driver MySQL** | `modulos_consultas/__init__.py:1` | `import pymysql` - Configuración PyMySQL |
| **Configuración BD** | `modulos_consultas/settings.py:120` | DATABASES config |
| **Variables de Entorno** | `modulos_consultas/settings.py:140` | DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT |
| **Migraciones** | `EduConnectApp/migrations/` | Historial de cambios |
| **Modelos** | `EduConnectApp/models.py` | 15 modelos con relaciones |

### 📊 Scripts de Base de Datos

```
test_mariadb.py                       → Probar conexión MySQL
check_mariadb.py                      → Verificar MariaDB
seed_mariadb_testdata.py              → Cargar datos de prueba
scripts/check_mariadb.py              → Script de verificación
```

### 🔄 Cambiar de BD

**Para SQLite (Desarrollo):**
```powershell
$env:USE_SQLITE = "1"
python manage.py runserver
```

**Para MySQL (Producción):**
```powershell
$env:USE_SQLITE = "0"
$env:DB_HOST = "localhost"
$env:DB_USER = "root"
$env:DB_PASSWORD = "admin"
python manage.py migrate
python manage.py runserver
```

---

## 🌐 3. API REST COMPLETA

### 📍 Ubicación de Vistas API

**Archivo:** `EduConnectApp/api/views.py` (líneas 1-50)

```python
from rest_framework import viewsets, permissions

class ConsultasViewSet(viewsets.ModelViewSet):
    """API completa para Consultas (CRUD)"""
    queryset = Consultas.objects.all()
    serializer_class = ConsultasSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RespuestasViewSet(viewsets.ModelViewSet):
    """API completa para Respuestas (CRUD)"""
    queryset = Respuestas.objects.all()
    serializer_class = RespuestasSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UsuariosViewSet(viewsets.ReadOnlyModelViewSet):
    """API de lectura para Usuarios"""
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# ... más ViewSets
```

### 📋 Endpoints API REST

#### Consultas
```
GET    /api/consultas/                     → Listar todas
GET    /api/consultas/{id}/                → Detalle consulta
POST   /api/consultas/                     → Crear consulta
PUT    /api/consultas/{id}/                → Actualizar completo
PATCH  /api/consultas/{id}/                → Actualizar parcial
DELETE /api/consultas/{id}/                → Eliminar
```

#### Respuestas
```
GET    /api/respuestas/                    → Listar todas
GET    /api/respuestas/{id}/               → Detalle respuesta
POST   /api/respuestas/                    → Crear respuesta
PUT    /api/respuestas/{id}/               → Actualizar completo
PATCH  /api/respuestas/{id}/               → Actualizar parcial
DELETE /api/respuestas/{id}/               → Eliminar
```

#### Usuarios
```
GET    /api/usuarios/                      → Listar usuarios
GET    /api/usuarios/{id}/                 → Detalle usuario (lectura)
```

#### Asignaturas
```
GET    /api/asignaturas/                   → Listar asignaturas
GET    /api/asignaturas/{id}/              → Detalle asignatura
POST   /api/asignaturas/                   → Crear asignatura
PUT    /api/asignaturas/{id}/              → Actualizar
DELETE /api/asignaturas/{id}/              → Eliminar
```

#### Categorías
```
GET    /api/categorias/                    → Listar categorías
GET    /api/categorias/{id}/               → Detalle categoría
POST   /api/categorias/                    → Crear categoría
PUT    /api/categorias/{id}/               → Actualizar
DELETE /api/categorias/{id}/               → Eliminar
```

#### Docentes
```
GET    /api/docentes/                      → Listar docentes
GET    /api/docentes/{id}/                 → Detalle docente
POST   /api/docentes/                      → Crear docente
PUT    /api/docentes/{id}/                 → Actualizar
DELETE /api/docentes/{id}/                 → Eliminar
```

### 🔒 Autenticación en API

#### 1. Token Authentication
```bash
# Obtener token
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username":"estudiante1", "password":"password123"}'

# Usar token en requests
curl http://localhost:8000/api/consultas/ \
  -H "Authorization: Token abc123def456"
```

#### 2. Session Authentication
```bash
# Autenticarse por sesión (login normal)
# El navegador mantiene la sesión automáticamente
```

### 📍 Ubicación de Serializers

**Archivo:** `EduConnectApp/api/serializers.py` (líneas 1-100+)

```python
class ConsultasSerializer(serializers.ModelSerializer):
    """Serializer para Consultas con validaciones"""
    class Meta:
        model = Consultas
        fields = ['id_consulta', 'titulo', 'descripcion', 'estado', ...]
        # Validaciones personalizadas
        
class RespuestasSerializer(serializers.ModelSerializer):
    """Serializer para Respuestas con validaciones"""
    # ... validaciones
```

### 📍 Ubicación de URLs API

**Archivo:** `EduConnectApp/api/urls.py`

```python
from rest_framework.routers import DefaultRouter
from .views import (
    ConsultasViewSet, RespuestasViewSet, UsuariosViewSet,
    AsignaturasViewSet, CategoriasViewSet, DocentesViewSet
)

router = DefaultRouter()
router.register(r'consultas', ConsultasViewSet)
router.register(r'respuestas', RespuestasViewSet)
router.register(r'usuarios', UsuariosViewSet)
router.register(r'asignaturas', AsignaturasViewSet)
router.register(r'categorias', CategoriasViewSet)
router.register(r'docentes', DocentesViewSet)

urlpatterns = router.urls
```

---

## 📤 4. RESULTADOS DE API EN JSON

### 📍 Ubicación de Serializers

**Archivo:** `EduConnectApp/api/serializers.py`

```python
# Line 1-20: Importes
from rest_framework import serializers
from ..models import Consultas, Respuestas, Usuarios, ...

# Line 25-70: UsuariosSerializer
class UsuariosSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = Usuarios
        fields = ['id_usuario', 'email', 'nombre', 'apellido_paterno', ...]

# Line 100-150: ConsultasSerializer
class ConsultasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultas
        fields = ['id_consulta', 'titulo', 'descripcion', 'estado', ...]

# Line 150-200: RespuestasSerializer
class RespuestasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuestas
        fields = ['id_respuesta', 'contenido', 'id_consulta', ...]
```

### 🎨 Ejemplo de Respuestas JSON

#### 1. Listar Consultas: `GET /api/consultas/`
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id_consulta": 1,
      "titulo": "¿Cómo resolver ecuaciones diferenciales?",
      "descripcion": "Tengo dudas con los métodos de resolución...",
      "estado": "pendiente",
      "prioridad": "alta",
      "fecha_consulta": "2025-11-30T10:30:00Z",
      "id_estudiante": 1,
      "id_asignatura": 3,
      "id_categoria": 5
    },
    {
      "id_consulta": 2,
      "titulo": "Duda sobre limites",
      "descripcion": "¿Cómo calcular limites indeterminados?",
      "estado": "respondida",
      "prioridad": "media",
      "fecha_consulta": "2025-11-29T14:20:00Z",
      "id_estudiante": 2,
      "id_asignatura": 3,
      "id_categoria": 4
    }
  ]
}
```

#### 2. Detalle de Consulta: `GET /api/consultas/1/`
```json
{
  "id_consulta": 1,
  "titulo": "¿Cómo resolver ecuaciones diferenciales?",
  "descripcion": "Tengo dudas con los métodos de resolución...",
  "estado": "pendiente",
  "prioridad": "alta",
  "fecha_consulta": "2025-11-30T10:30:00Z",
  "fecha_limite_respuesta": "2025-12-05T10:30:00Z",
  "es_anonima": 0,
  "id_estudiante": 1,
  "id_asignatura": 3,
  "id_categoria": 5,
  "respuestas_count": 2,
  "created_at": "2025-11-30T10:30:00Z",
  "updated_at": "2025-11-30T11:45:00Z"
}
```

#### 3. Crear Consulta: `POST /api/consultas/` (Body JSON)
```json
{
  "titulo": "Duda sobre integración",
  "descripcion": "¿Cuál es el método correcto para integración por partes?",
  "prioridad": "media",
  "estado": "pendiente",
  "id_estudiante": 1,
  "id_asignatura": 3,
  "id_categoria": 5,
  "fecha_limite_respuesta": "2025-12-10"
}
```

#### 4. Respuesta API: `201 Created`
```json
{
  "id_consulta": 6,
  "titulo": "Duda sobre integración",
  "descripcion": "¿Cuál es el método correcto para integración por partes?",
  "prioridad": "media",
  "estado": "pendiente",
  "fecha_consulta": "2025-11-30T15:00:00Z",
  "fecha_limite_respuesta": "2025-12-10T00:00:00Z",
  "id_estudiante": 1,
  "id_asignatura": 3,
  "id_categoria": 5,
  "created_at": "2025-11-30T15:00:00Z"
}
```

#### 5. Listar Respuestas: `GET /api/respuestas/`
```json
{
  "count": 8,
  "results": [
    {
      "id_respuesta": 1,
      "contenido": "Para resolver ecuaciones diferenciales lineales de primer orden...",
      "tipo_respuesta": "academica",
      "calificacion": {
        "claridad": 5,
        "exactitud": 5,
        "utilidad": 4
      },
      "id_consulta": 1,
      "id_docente": 1,
      "fecha_respuesta": "2025-11-30T14:20:00Z",
      "es_aceptada": 1
    }
  ]
}
```

#### 6. Listar Usuarios: `GET /api/usuarios/`
```json
{
  "count": 25,
  "results": [
    {
      "id_usuario": 1,
      "email": "estudiante1@universidad.edu",
      "tipo_usuario": "estudiante",
      "nombre": "Juan",
      "apellido_paterno": "Pérez",
      "apellido_materno": "García",
      "nombre_completo": "Juan Pérez García",
      "telefono": "+56987654321",
      "estado": "activo"
    },
    {
      "id_usuario": 2,
      "email": "docente1@universidad.edu",
      "tipo_usuario": "docente",
      "nombre": "María",
      "apellido_paterno": "López",
      "apellido_materno": "Rodríguez",
      "nombre_completo": "María López Rodríguez",
      "telefono": "+56912345678",
      "estado": "activo"
    }
  ]
}
```

#### 7. Error 404: `GET /api/consultas/999/`
```json
{
  "detail": "Not found."
}
```

#### 8. Error de Validación: `POST /api/consultas/` (falta campo requerido)
```json
{
  "titulo": ["This field is required."],
  "id_estudiante": ["This field is required."],
  "id_asignatura": ["This field is required."]
}
```

### 📍 Ubicación de Configuración JSON

**Archivo:** `modulos_consultas/settings.py` (líneas 246-260)

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ]
}
```

---

## 🔌 5. APIS EXTERNAS

### 📍 Ubicación

**Archivos con llamadas HTTP:**
- `scripts/test_api_calls.py` - Pruebas de API
- `scripts/web_create_test_requests.py` - Crear consultas via HTTP
- `scripts/web_create_test_consulta.py` - Crear consultas con urllib
- `EduConnectApp/views.py` - Vistas que consumen APIs

### 🌍 Ejemplos de Integración Externa

#### 1. Script de Prueba API: `scripts/test_api_calls.py`

```python
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

# Cliente API
client = APIClient()

# 1. Obtener token
token = Token.objects.get(user__username='usuario1')
client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

# 2. Hacer requests GET
response = client.get('/api/consultas/')
data = response.json()

# 3. Hacer requests POST
new_consulta = {
    'titulo': 'Nueva consulta',
    'descripcion': 'Descripción...',
    'id_estudiante': 1,
    'id_asignatura': 3
}
response = client.post('/api/consultas/', new_consulta, format='json')
print(response.json())
```

#### 2. Consumir API Externa con `requests`: `scripts/web_create_test_requests.py`

```python
import requests

base_url = 'http://127.0.0.1:8000'
session = requests.Session()

# Login
login_url = f'{base_url}/login/'
login_data = {'email': 'estudiante1@universidad.edu', 'password': 'password123'}
response = session.post(login_url, data=login_data)

# Crear consulta
consulta_data = {
    'titulo': 'Consulta via requests',
    'descripcion': 'Descripción desde script',
    'id_asignatura': 1,
    'prioridad': 'media'
}
response = session.post(f'{base_url}/consultas/crear/', data=consulta_data)
print(response.json())
```

#### 3. Consumir API con urllib: `scripts/web_create_test_consulta.py`

```python
import http.cookiejar
import urllib.request
import urllib.parse
import json

# Manejo de cookies
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

base_url = 'http://127.0.0.1:8000'

# Login
login_data = urllib.parse.urlencode({
    'email': 'estudiante1@universidad.edu',
    'password': 'password123'
}).encode('utf-8')

req = urllib.request.Request(f'{base_url}/login/', data=login_data)
response = opener.open(req)

# GET CSRF token
req = urllib.request.Request(f'{base_url}/consultas/crear/')
response = opener.open(req)
html = response.read().decode('utf-8')

# Crear consulta
consulta_data = urllib.parse.urlencode({
    'titulo': 'Consulta via urllib',
    'descripcion': 'Descripción desde urllib'
}).encode('utf-8')

req = urllib.request.Request(f'{base_url}/consultas/crear/', data=consulta_data)
response = opener.open(req)
print(response.read().decode('utf-8'))
```

### 🔗 Endpoint para Consumir la API

```bash
# Desde otra aplicación o cliente
curl -X GET http://localhost:8000/api/consultas/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json"

# Resultado: JSON con las consultas
```

---

## 📚 6. DOCUMENTACIÓN API

### 📍 Ubicación

**Archivos:**
- `modulos_consultas/urls.py` - URLs de documentación
- `EduConnectApp/api/serializers.py` - Docstrings de serializers
- `EduConnectApp/api/views.py` - Docstrings de ViewSets

### 🎨 Acceso a Documentación

#### 1. Swagger UI
```
http://localhost:8000/api/docs/
```

#### 2. Esquema OpenAPI JSON
```
http://localhost:8000/api/schema/
```

#### 3. Admin Django
```
http://localhost:8000/admin/
```

### 📖 Archivos de Documentación

```
README.md                              → Introducción general
README_INICIO_RAPIDO.md                → Guía de inicio
SECURITY_IMPROVEMENTS.md               → Mejoras de seguridad
GUIA_ACCESO_RED.md                     → Acceso desde red local
CREDENCIALES.md                        → Usuarios de prueba
SISTEMA_PERMISOS.md                    → Sistema de permisos
```

---

## 🧪 7. SCRIPTS DE PRUEBA

### 📍 Ubicación

**Carpeta:** `scripts/` y raíz del proyecto

### 📋 Scripts Disponibles

| Script | Propósito | Ubicación |
|--------|-----------|-----------|
| `test_api_calls.py` | Pruebas API REST | `scripts/` |
| `web_create_test_requests.py` | Crear consultas via HTTP | `scripts/` |
| `web_create_test_consulta.py` | Crear consultas con urllib | `scripts/` |
| `test_security.py` | Verificar configuraciones | Raíz |
| `test_funcionamiento.py` | Pruebas funcionales | Raíz |
| `test_mariadb.py` | Probar conexión MySQL | Raíz |
| `resumen_sistema.py` | Resumen del sistema | Raíz |
| `verificar_y_crear_admin.py` | Crear usuario admin | Raíz |
| `listar_cuentas.py` | Listar usuarios | Raíz |

### ▶️ Ejecutar Scripts

```powershell
# Pruebas de API
python scripts/test_api_calls.py

# Verificar seguridad
python test_security.py

# Resumen del sistema
python resumen_sistema.py

# Listar usuarios
python listar_cuentas.py
```

---

## 🚀 RESUMEN RÁPIDO

### ✅ Control de Usuarios
- **Modelo:** `EduConnectApp/models.py` (línea 160)
- **Autenticación:** `EduConnectApp/views.py` (línea 200)
- **Permisos:** `EduConnectApp/decorators.py`

### ✅ Base de Datos MySQL
- **Configuración:** `modulos_consultas/settings.py` (línea 120)
- **Driver:** `modulos_consultas/__init__.py` (PyMySQL)
- **Scripts:** `test_mariadb.py`, `check_mariadb.py`

### ✅ API REST
- **ViewSets:** `EduConnectApp/api/views.py`
- **Serializers:** `EduConnectApp/api/serializers.py`
- **URLs:** `EduConnectApp/api/urls.py`
- **Documentación:** `http://localhost:8000/api/docs/`

### ✅ Respuestas JSON
- **Generadas por:** Serializers de Django REST Framework
- **Ubicación:** `EduConnectApp/api/serializers.py`
- **Ejemplos:** Ver sección 4

### ✅ APIs Externas
- **Cliente HTTP:** `requests` y `urllib` libraries
- **Scripts de prueba:** `scripts/web_create_test_requests.py`
- **Integración:** Vistas en `EduConnectApp/views.py`

---

## 📞 CONTACTO Y SOPORTE

Para más información sobre algún componente específico, consulta:
- Los comentarios en los archivos `.py`
- Los archivos `.md` de documentación
- Los scripts de ejemplo en `scripts/`

**Última actualización:** 30/11/2025
