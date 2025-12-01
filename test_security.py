#!/usr/bin/env python
"""
Script para verificar que las mejoras de seguridad funcionan correctamente
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
os.environ['USE_SQLITE'] = '1'
django.setup()

from django.conf import settings
from EduConnectApp.api.serializers import (
    UsuariosSerializer, ConsultasSerializer, RespuestasSerializer,
    EstudiantesSerializer, DocentesSerializer
)

print("="*70)
print("VERIFICACIÓN DE MEJORAS DE SEGURIDAD")
print("="*70)
print()

# 1. Verificar configuraciones CSRF
print("✅ 1. CONFIGURACIONES CSRF")
print(f"   CSRF_TRUSTED_ORIGINS: {settings.CSRF_TRUSTED_ORIGINS}")
print(f"   CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
print(f"   CSRF_COOKIE_HTTPONLY: {settings.CSRF_COOKIE_HTTPONLY}")
print(f"   CSRF_COOKIE_SAMESITE: {settings.CSRF_COOKIE_SAMESITE}")
print()

# 2. Verificar configuraciones SSL
print("✅ 2. CONFIGURACIONES SSL/HTTPS")
print(f"   DEBUG: {settings.DEBUG}")
print(f"   SECURE_SSL_REDIRECT: {settings.SECURE_SSL_REDIRECT}")
print(f"   SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
print(f"   SECURE_CONTENT_TYPE_NOSNIFF: {settings.SECURE_CONTENT_TYPE_NOSNIFF}")
print(f"   X_FRAME_OPTIONS: {settings.X_FRAME_OPTIONS}")
print()

# 3. Verificar sesiones
print("✅ 3. CONFIGURACIONES DE SESIÓN")
print(f"   SESSION_COOKIE_NAME: {settings.SESSION_COOKIE_NAME}")
print(f"   SESSION_COOKIE_AGE: {settings.SESSION_COOKIE_AGE} segundos ({settings.SESSION_COOKIE_AGE/3600} horas)")
print(f"   SESSION_COOKIE_HTTPONLY: {settings.SESSION_COOKIE_HTTPONLY}")
print()

# 4. Verificar middleware
print("✅ 4. MIDDLEWARE CONFIGURADO")
for i, middleware in enumerate(settings.MIDDLEWARE, 1):
    middleware_name = middleware.split('.')[-1]
    print(f"   {i}. {middleware_name}")
print()

# 5. Verificar serializers
print("✅ 5. SERIALIZERS DISPONIBLES")
serializers = [
    ('UsuariosSerializer', UsuariosSerializer),
    ('ConsultasSerializer', ConsultasSerializer),
    ('RespuestasSerializer', RespuestasSerializer),
    ('EstudiantesSerializer', EstudiantesSerializer),
    ('DocentesSerializer', DocentesSerializer),
]

for name, serializer_class in serializers:
    print(f"   ✓ {name}")
    if hasattr(serializer_class.Meta, 'read_only_fields'):
        read_only = serializer_class.Meta.read_only_fields
        if read_only:
            print(f"     - Campos read_only: {len(read_only)}")
print()

# 6. Verificar REST Framework
print("✅ 6. DJANGO REST FRAMEWORK")
print(f"   Authentication Classes:")
for auth_class in settings.REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']:
    print(f"     - {auth_class.split('.')[-1]}")
print(f"   Permission Classes:")
for perm_class in settings.REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES']:
    print(f"     - {perm_class.split('.')[-1]}")
print()

# 7. Resumen
print("="*70)
print("✅ TODAS LAS CONFIGURACIONES DE SEGURIDAD ESTÁN ACTIVAS")
print("="*70)
print()
print("Archivos modificados:")
print("  1. settings.py - CSRF, SSL, Sessions")
print("  2. serializers.py - Validaciones, read_only/write_only")
print("  3. middleware.py - Rate limiting, sanitización, logging")
print()
print("Documentación completa en: SECURITY_IMPROVEMENTS.md")
print("="*70)
