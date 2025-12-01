# 🔒 Mejoras de Seguridad Implementadas

## Resumen
Se han implementado mejoras significativas de seguridad en el proyecto Django, incluyendo protección CSRF, SSL/HTTPS, serializers optimizados y middleware de seguridad personalizado.

---

## 🛡️ 1. Protección CSRF (Cross-Site Request Forgery)

### Configuraciones Implementadas en `settings.py`:

```python
# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://192.168.1.13:8000',
]

# Configuración según entorno
if not DEBUG:
    CSRF_COOKIE_SECURE = True      # Solo HTTPS
    CSRF_COOKIE_HTTPONLY = True    # No accesible via JavaScript
    CSRF_COOKIE_SAMESITE = 'Strict'  # Máxima protección
else:
    CSRF_COOKIE_SECURE = False     # Permitir HTTP en desarrollo
    CSRF_COOKIE_HTTPONLY = False   # Accesible en desarrollo
    CSRF_COOKIE_SAMESITE = 'Lax'   # Más permisivo

CSRF_COOKIE_AGE = 31449600  # 1 año
```

### ¿Qué protege?
- ✅ Previene ataques donde un sitio malicioso intenta realizar acciones en nombre del usuario
- ✅ Valida que las peticiones POST/PUT/DELETE provengan de orígenes confiables
- ✅ Protege cookies contra acceso no autorizado

---

## 🔐 2. Configuración SSL/HTTPS

### Configuraciones en Producción (`DEBUG = False`):

```python
SECURE_SSL_REDIRECT = True                 # Forzar HTTPS
SECURE_HSTS_SECONDS = 31536000            # HSTS por 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True     # Incluir subdominios
SECURE_HSTS_PRELOAD = True                # Preload HSTS
SESSION_COOKIE_SECURE = True              # Cookies solo via HTTPS
SECURE_CONTENT_TYPE_NOSNIFF = True        # Prevenir MIME sniffing
SECURE_BROWSER_XSS_FILTER = True          # Filtro XSS del navegador
X_FRAME_OPTIONS = 'DENY'                  # Prevenir clickjacking
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### ¿Qué protege?
- ✅ Fuerza todas las conexiones a usar HTTPS encriptado
- ✅ Protege contra downgrade attacks
- ✅ Previene clickjacking y MIME type sniffing
- ✅ Habilita filtros XSS del navegador

---

## 📋 3. Configuración de Sesiones

```python
SESSION_COOKIE_NAME = 'educonnect_sessionid'
SESSION_COOKIE_AGE = 86400  # 24 horas
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax' if DEBUG else 'Strict'
```

### ¿Qué protege?
- ✅ Sesiones expiran automáticamente después de 24 horas
- ✅ Cookies de sesión no accesibles via JavaScript
- ✅ Protección contra ataques CSRF en sesiones

---

## 🎯 4. Serializers Mejorados

### Características Implementadas:

#### ✅ Campos Read-Only / Write-Only
```python
# Ejemplo: ConsultasSerializer
class ConsultasSerializer(serializers.ModelSerializer):
    # Read-only: información completa del objeto relacionado
    estudiante = EstudiantesSerializer(source='id_estudiante', read_only=True)
    
    # Write-only: solo ID para creación/actualización
    estudiante_id = serializers.PrimaryKeyRelatedField(
        queryset=Estudiantes.objects.all(),
        source='id_estudiante',
        write_only=True
    )
```

**Beneficios:**
- 🔒 Previene exposición de datos sensibles
- 🔒 Evita modificación de campos calculados
- 🔒 Separa información de lectura vs escritura

#### ✅ Validaciones Personalizadas
```python
def validate_email(self, value):
    """Valida formato de email"""
    if value and not '@' in value:
        raise serializers.ValidationError("Email inválido")
    return value.lower()

def validate_prioridad(self, value):
    """Valida valores permitidos"""
    prioridades_validas = ['alta', 'media', 'baja', 'urgente']
    if value and value not in prioridades_validas:
        raise serializers.ValidationError(
            f"Prioridad inválida. Debe ser una de: {', '.join(prioridades_validas)}"
        )
    return value
```

**Beneficios:**
- ✅ Validación de datos en la capa de API
- ✅ Mensajes de error claros y descriptivos
- ✅ Previene inyección de datos inválidos

#### ✅ Exclusión de Campos Sensibles
```python
class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = [
            'id_usuario', 'email', 'tipo_usuario', 'nombre', 
            'apellido_paterno', 'apellido_materno', 'telefono',
            'foto_perfil', 'estado', 'nombre_completo'
        ]
        # ❌ NUNCA expone: password_hash, tokens, etc.
```

**Beneficios:**
- 🔒 NUNCA expone passwords ni información sensible
- 🔒 Control granular de qué datos se pueden leer/escribir
- 🔒 Diferentes serializers para diferentes niveles de acceso

#### ✅ Serializers Especializados
- `ConsultasListSerializer` - Ligero para listados
- `ConsultasSerializer` - Completo para detalles
- `UsuariosSerializer` - Público
- `UsuariosDetailSerializer` - Con más información para autenticados

---

## 🛡️ 5. Middleware de Seguridad

### 5.1. SecurityHeadersMiddleware
**Función:** Añade headers de seguridad HTTP

```python
# Headers añadidos automáticamente:
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'...
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()...
```

**Beneficios:**
- ✅ Previene ataques XSS (Cross-Site Scripting)
- ✅ Control de qué recursos puede cargar la página
- ✅ Deshabilita funciones del navegador no necesarias
- ✅ Protege contra MIME type sniffing

### 5.2. RateLimitMiddleware
**Función:** Limita peticiones por IP para prevenir ataques

```python
# Configuración por defecto:
MAX_REQUESTS = 100 peticiones / 60 segundos

# Endpoints sensibles con límites más estrictos:
'/login/': 5 peticiones / 60 segundos
'/api/auth/login/': 5 peticiones / 60 segundos
'/password-reset/': 3 peticiones / 300 segundos
'/api/': 50 peticiones / 60 segundos
```

**Beneficios:**
- ✅ Previene ataques de fuerza bruta en login
- ✅ Protege contra ataques DoS/DDoS
- ✅ Registra intentos sospechosos en logs
- ✅ Respuestas HTTP 429 cuando se excede el límite

### 5.3. InputSanitizationMiddleware
**Función:** Valida y sanitiza inputs para prevenir inyección

```python
# Patrones peligrosos detectados:
- <script> tags
- javascript: URLs
- Event handlers (onclick, onload, etc.)
- <iframe>, <object>, <embed> tags
```

**Beneficios:**
- ✅ Previene ataques XSS (Cross-Site Scripting)
- ✅ Detecta intentos de inyección de código
- ✅ Bloquea peticiones con contenido malicioso
- ✅ Registra intentos de ataque en logs

### 5.4. ActivityLogMiddleware
**Función:** Registra actividad de usuarios para auditoría

```python
# Registra:
- Todos los métodos POST, PUT, PATCH, DELETE
- Accesos a /api/, /login/, /logout/, /admin/
- IP del cliente, User Agent
- Status code de la respuesta
```

**Beneficios:**
- ✅ Auditoría completa de acciones importantes
- ✅ Rastreo de actividad sospechosa
- ✅ Útil para debugging y análisis forense
- ✅ Cumplimiento de normativas (GDPR, etc.)

### 5.5. EnsureUsuarioSessionMiddleware (Mejorado)
**Función:** Sincroniza sesión Django con modelo Usuarios

```python
# Funcionalidad añadida:
- Actualiza último_acceso automáticamente
- Mejor manejo de errores
- Logging de problemas
```

---

## 📊 6. REST Framework Security

### Configuración en `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
```

**Beneficios:**
- ✅ Autenticación por token para APIs
- ✅ Soporte para sesiones web
- ✅ Permisos basados en modelo Django
- ✅ Usuarios no autenticados solo lectura

---

## 🚀 7. Cómo Usar en Producción

### Paso 1: Configurar Variables de Entorno
```bash
# .env file
DEBUG=False
SECRET_KEY=<tu-secret-key-seguro>
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
CSRF_TRUSTED_ORIGINS=https://tudominio.com,https://www.tudominio.com
```

### Paso 2: Configurar HTTPS
- Usar certificado SSL (Let's Encrypt, etc.)
- Configurar servidor web (Nginx, Apache)
- Habilitar redirección HTTP → HTTPS

### Paso 3: Base de Datos Segura
```bash
# Variables de entorno para DB
DB_NAME=tu_base_datos
DB_USER=usuario_seguro
DB_PASSWORD=password_complejo_123!
DB_HOST=localhost
DB_PORT=3306
```

### Paso 4: Configurar Cache (para Rate Limiting)
```python
# En settings.py para producción
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

---

## 🧪 8. Testing de Seguridad

### Verificar CSRF
```bash
curl -X POST http://localhost:8000/api/consultas/ \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Test"}'
# Debe retornar error 403 sin token CSRF
```

### Verificar Rate Limiting
```bash
# Hacer múltiples peticiones rápidas
for i in {1..10}; do
  curl http://localhost:8000/login/
done
# Debe retornar 429 después del límite
```

### Verificar Headers de Seguridad
```bash
curl -I http://localhost:8000/
# Verificar presencia de headers:
# X-Content-Type-Options: nosniff
# Content-Security-Policy: ...
# Referrer-Policy: same-origin
```

---

## 📚 9. Referencias y Recursos

### Django Security
- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django REST Framework Security](https://www.django-rest-framework.org/topics/security/)

### Headers de Seguridad
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [HSTS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)
- [Security Headers Best Practices](https://securityheaders.com/)

---

## ⚠️ 10. Notas Importantes

### Desarrollo vs Producción
- 🔴 **Desarrollo (DEBUG=True)**: Configuraciones permisivas para facilitar desarrollo
- 🟢 **Producción (DEBUG=False)**: Todas las protecciones activadas

### Mantenimiento
- 🔄 Revisar logs regularmente: `LogsActividad`
- 🔄 Actualizar `CSRF_TRUSTED_ORIGINS` cuando cambies dominios
- 🔄 Monitorear rate limits y ajustar si es necesario
- 🔄 Revisar y actualizar patrones de sanitización

### Personalización
Todos los límites y configuraciones pueden ajustarse en:
- `settings.py` - Configuraciones globales
- `middleware.py` - Límites de rate limiting, patrones peligrosos, etc.
- `serializers.py` - Validaciones personalizadas

---

## ✅ Checklist de Seguridad

- [x] CSRF Protection configurado
- [x] SSL/HTTPS settings para producción
- [x] Rate limiting implementado
- [x] Input sanitization activo
- [x] Security headers configurados
- [x] Activity logging habilitado
- [x] Serializers con validaciones
- [x] Campos sensibles protegidos
- [x] Sesiones seguras configuradas
- [x] Permisos REST Framework
- [ ] Certificado SSL instalado (producción)
- [ ] Backup automático de base de datos
- [ ] Monitoreo de logs configurado
- [ ] Pruebas de penetración realizadas

---

**Fecha de Implementación:** 2025-11-04  
**Versión:** 1.0.0  
**Mantenedor:** GitHub Copilot
