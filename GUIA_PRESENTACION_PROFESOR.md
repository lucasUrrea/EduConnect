# 📍 UBICACIÓN DE IMPLEMENTACIONES - GUÍA PARA PRESENTACIÓN

## 🎯 REQUISITOS DEL PROYECTO - UBICACIÓN EN EL CÓDIGO

---

## 1. SISTEMA DE LOGIN, LOGOUT Y REGISTRO

### **Login**
📂 **Archivo:** `EduConnectApp/views.py`
📍 **Líneas:** 66-145
```python
@csrf_protect
def login_view(request):
    """Vista de login personalizada"""
    # POST method - validación de credenciales
    # GET method - mostrar formulario
```

**Qué mostrar al profesor:**
- Autenticación con Django (`authenticate()`, `auth_login()`)
- Autenticación custom con tabla `Usuarios`
- Validación de contraseña con `check_password()`
- Verificación de usuario activo
- Redirección según rol

### **Logout**
📂 **Archivo:** `EduConnectApp/views.py`
📍 **Buscar:** `def logout_view(request)`
```python
def logout_view(request):
    """Cierre de sesión"""
    logout(request)
    return redirect('login')
```

### **Registro (si existe)**
📂 **Archivo:** `EduConnectApp/views.py`
📍 **Buscar:** funciones relacionadas con registro/signup

---

## 2. PANEL O VISTA PROTEGIDA (SOLO CON SESIÓN ACTIVA)

### **Dashboard Estudiante (Protegido)**
📂 **Archivo:** `EduConnectApp/views.py`
📍 **Buscar:** `def dashboard_estudiante(request)`
```python
def dashboard_estudiante(request):
    # Verificación de autenticación
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Verificación de sesión
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
```

### **Dashboard Docente (Protegido)**
📂 **Archivo:** `EduConnectApp/views.py`
📍 **Buscar:** `def dashboard_docente(request)`

### **Templates Protegidos**
📂 **Archivos:**
- `EduConnectApp/templates/EduConnectApp/dashboard_estudiante.html`
- `EduConnectApp/templates/EduConnectApp/dashboard_docente.html`

**Qué mostrar:**
- Solo accesibles con `request.user.is_authenticated`
- Requieren `usuario_id` en sesión

---

## 3. CONTROL DE SESIONES ACTIVAS

### **Middleware de Sesión**
📂 **Archivo:** `EduConnectApp/middleware.py`
📍 **Líneas:** 10-35
```python
class EnsureUsuarioSessionMiddleware(MiddlewareMixin):
    """
    Ensure that when a Django user is authenticated, the session contains
    the corresponding Usuarios.id_usuario and tipo_usuario values.
    """
```

**Qué explicar:**
- Sincroniza usuario Django con sesión personalizada
- Guarda `usuario_id`, `tipo_usuario`, `nombre_completo` en `request.session`
- Actualiza `ultimo_acceso` del usuario

### **Configuración de Sesiones**
📂 **Archivo:** `modulos_consultas/settings.py`
📍 **Buscar:** variables de sesión
```python
SESSION_COOKIE_AGE = ...  # Tiempo de vida de sesión
SESSION_EXPIRE_AT_BROWSER_CLOSE = ...  # Expira al cerrar navegador
SESSION_COOKIE_HTTPONLY = True  # Protección XSS
SESSION_COOKIE_SAMESITE = 'Lax'  # Protección CSRF
```

### **Uso de Sesiones en Views**
📂 **Archivo:** `EduConnectApp/views.py`
📍 **Ejemplo en login_view (líneas ~81-83):**
```python
request.session['usuario_id'] = perfil.id_usuario
request.session['tipo_usuario'] = perfil.tipo_usuario
request.session['nombre_completo'] = f"{perfil.nombre} {perfil.apellido_paterno}"
```

---

## 4. CONFIGURACIÓN DE SEGURIDAD EN SETTINGS.PY

📂 **Archivo:** `modulos_consultas/settings.py`

### **A) Seguridad Básica**
📍 **Buscar estas variables:**
```python
DEBUG = True  # En producción debe ser False

SECRET_KEY = 'django-insecure-...'  # Clave secreta

ALLOWED_HOSTS = ['*']  # En producción, lista específica

# Seguridad de cookies
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Seguridad adicional
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

### **B) Middlewares de Seguridad**
📍 **Líneas:** 120-133
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'EduConnectApp.middleware.EnsureUsuarioSessionMiddleware',
    'EduConnectApp.middleware.RateLimitMiddleware',
    'EduConnectApp.middleware.InputSanitizationMiddleware',
    'EduConnectApp.middleware.SecurityHeadersMiddleware',
    ...
]
```

### **C) Sistema de Autenticación**
📍 **Buscar:**
```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

---

## 5. VALIDACIONES DE ENTRADA EN FORMULARIOS

### **A) Validación CSRF**
📂 **Archivo:** `EduConnectApp/views.py`
📍 **En todas las vistas con POST:**
```python
@csrf_protect
def login_view(request):
    # CSRF token validado automáticamente
```

### **B) Formularios Django**
📂 **Archivo:** `EduConnectApp/forms.py`
📍 **Líneas completas del archivo**
```python
class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consultas
        fields = [...]
        
    def clean_titulo(self):
        # Validación personalizada
        
class RespuestaForm(forms.ModelForm):
    # Validaciones de campos
```

### **C) Sanitización de Inputs**
📂 **Archivo:** `EduConnectApp/middleware.py`
📍 **Líneas:** 165-215
```python
class InputSanitizationMiddleware(MiddlewareMixin):
    """
    Middleware para sanitizar y validar inputs.
    Previene ataques de inyección SQL, XSS, y otros.
    """
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        ...
    ]
```

---

## 6. CONTROLES DE USUARIO CON DJANGO ADMIN

### **A) Registro de Modelos en Admin**
📂 **Archivo:** `EduConnectApp/admin.py`
📍 **Todo el archivo**
```python
@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ['email', 'nombre', 'tipo_usuario', 'estado']
    list_filter = ['tipo_usuario', 'estado']
    search_fields = ['email', 'nombre']
    
@admin.register(Estudiantes)
class EstudiantesAdmin(admin.ModelAdmin):
    ...
    
@admin.register(Docentes)
class DocentesAdmin(admin.ModelAdmin):
    ...
```

### **B) Acceso al Panel de Admin**
📂 **URL:** `http://localhost:8000/admin/`
📂 **Credenciales:** Ver `CREDENCIALES.md`
```
Usuario: admin
Password: admin123
```

### **C) Configuración de Admin**
📂 **Archivo:** `modulos_consultas/settings.py`
📍 **Buscar:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',  # Panel de administración
    ...
]
```

📂 **Archivo:** `modulos_consultas/urls.py`
📍 **Buscar:**
```python
urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta del admin
    ...
]
```

---

## 📊 CONTENIDO PARA EL INFORME

### **A) ANÁLISIS DEL PROBLEMA**
📂 **Consultar:** `README.md` o `RESUMEN_SISTEMA.md`
- Sistema necesita diferenciar entre estudiantes y docentes
- Control de acceso por roles
- Seguridad de datos académicos

### **B) FLUJO DE AUTENTICACIÓN**
📂 **Archivo:** `DIAGRAMA_FLUJO_LOGIN.md`
- Diagramas completos del flujo
- Proceso paso a paso
- Validaciones en cada etapa

### **C) USO DE SESIONES (request.session)**

**Guardar en sesión:**
📂 **Archivo:** `EduConnectApp/views.py` - `login_view`
```python
request.session['usuario_id'] = perfil.id_usuario
request.session['tipo_usuario'] = perfil.tipo_usuario
request.session['nombre_completo'] = f"{perfil.nombre} {perfil.apellido_paterno}"
```

**Leer de sesión:**
📂 **Archivo:** `EduConnectApp/views.py` - Cualquier vista
```python
usuario_id = request.session.get('usuario_id')
tipo_usuario = request.session.get('tipo_usuario')
```

**Eliminar sesión:**
📂 **Archivo:** `EduConnectApp/views.py` - `logout_view`
```python
logout(request)  # Limpia la sesión automáticamente
```

### **D) CONFIGURACIONES DE SEGURIDAD**

#### **1. Hashing de Contraseñas**
📂 **Archivo:** `EduConnectApp/views.py`
```python
# Al verificar login:
check_password(password, usuario.password_hash)

# Al crear usuario:
from django.contrib.auth.hashers import make_password
django_user.set_password(password)
```

📂 **Configuración:** `modulos_consultas/settings.py`
```python
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    ...
]
```

#### **2. CSRF Prevention**
📂 **Archivo:** `EduConnectApp/views.py`
```python
@csrf_protect  # Decorador en vistas
def login_view(request):
    ...
```

📂 **Template:** Cualquier formulario
```html
<form method="POST">
    {% csrf_token %}  <!-- Token CSRF -->
    ...
</form>
```

📂 **Middleware:** `modulos_consultas/settings.py`
```python
'django.middleware.csrf.CsrfViewMiddleware',  # En MIDDLEWARE
```

#### **3. Variables de Entorno y Ocultamiento de Claves**
📂 **Archivo:** `modulos_consultas/settings.py`
```python
import os

# Leer desde variable de entorno
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default')

# Base de datos según entorno
USE_SQLITE = os.environ.get('USE_SQLITE', '0') == '1'

if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            ...
        }
    }
```

📂 **Uso:**
```powershell
# En terminal antes de ejecutar
$env:USE_SQLITE='1'
python manage.py runserver
```

---

## 🎤 GUÍA RÁPIDA PARA LA PRESENTACIÓN

### **DEMOSTRACIÓN EN VIVO:**

1. **Login System** (2 min)
   - Mostrar `EduConnectApp/views.py` línea 66
   - Explicar flujo: autenticación → sesión → redirección
   - Mostrar template `login.html` con `{% csrf_token %}`

2. **Panel Protegido** (2 min)
   - Mostrar dashboard_estudiante en `views.py`
   - Mostrar validación: `if not request.user.is_authenticated`
   - Demo: intentar acceder sin login → redirige

3. **Control de Sesiones** (2 min)
   - Mostrar `EnsureUsuarioSessionMiddleware` en `middleware.py`
   - Explicar `request.session['usuario_id']`
   - Mostrar configuración en `settings.py`

4. **Seguridad** (3 min)
   - Abrir `settings.py`, mostrar:
     * `SESSION_COOKIE_HTTPONLY = True`
     * `CSRF_COOKIE_HTTPONLY = True`
     * Middlewares de seguridad
   - Mostrar `InputSanitizationMiddleware`
   - Mostrar hashing: `check_password()` en views.py

5. **Validaciones** (2 min)
   - Mostrar `forms.py` con validaciones
   - Mostrar `@csrf_protect` en views
   - Mostrar patrones peligrosos en middleware

6. **Django Admin** (2 min)
   - Abrir navegador: http://localhost:8000/admin/
   - Login con admin/admin123
   - Mostrar gestión de usuarios
   - Mostrar `admin.py` con registro de modelos

---

## 📋 CHECKLIST PARA LA PRESENTACIÓN

✅ **Archivos a tener abiertos:**
- [ ] `EduConnectApp/views.py` (login_view)
- [ ] `EduConnectApp/middleware.py` (EnsureUsuarioSessionMiddleware)
- [ ] `modulos_consultas/settings.py` (configuración de seguridad)
- [ ] `EduConnectApp/forms.py` (validaciones)
- [ ] `EduConnectApp/admin.py` (control de usuarios)
- [ ] `DIAGRAMA_FLUJO_LOGIN.md` (flujos visuales)

✅ **Navegador con pestañas:**
- [ ] http://localhost:8000/login/ (demo login)
- [ ] http://localhost:8000/admin/ (django admin)
- [ ] http://localhost:8000/dashboard/estudiante/ (panel protegido)

✅ **Terminal:**
- [ ] Servidor corriendo: `python manage.py runserver 0.0.0.0:8000`

---

## 🎯 PUNTOS CLAVE A MENCIONAR

1. **Sistema de Login:** Doble autenticación (Django + Custom)
2. **Sesiones:** `request.session` para almacenar datos del usuario
3. **Protección:** Vistas verifican autenticación antes de mostrar contenido
4. **Seguridad:** CSRF tokens, hashing de contraseñas, middlewares
5. **Validaciones:** Formularios Django + sanitización de inputs
6. **Admin:** Panel completo para gestionar usuarios y roles
7. **Diferenciación:** Estudiantes vs Docentes con diferentes permisos

---

**¡Éxito en tu presentación!** 🚀
