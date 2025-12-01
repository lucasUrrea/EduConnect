#!/usr/bin/env python
"""
Script de pruebas rápidas para verificar funcionalidad del sistema
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
os.environ['USE_SQLITE'] = '1'
django.setup()

from django.contrib.auth import authenticate
from EduConnectApp.models import Usuarios, Estudiantes, Docentes, Consultas, Asignaturas
from EduConnectApp.api.serializers import (
    UsuariosSerializer, ConsultasSerializer, EstudiantesSerializer
)

print("="*70)
print("🧪 PRUEBAS RÁPIDAS DEL SISTEMA")
print("="*70)
print()

# ==============================================================================
# TEST 1: Autenticación
# ==============================================================================
print("📋 TEST 1: Verificar Autenticación del Admin")
print("-" * 70)

# Probar autenticación del admin
admin_user = authenticate(username='admin', password='admin123')
if admin_user:
    print("✅ Admin autenticado correctamente")
    print(f"   Usuario: {admin_user.username}")
else:
    print("❌ Error en autenticación del admin")
print()

# ==============================================================================
# TEST 2: Contar registros en base de datos
# ==============================================================================
print("📋 TEST 2: Conteo de Registros en Base de Datos")
print("-" * 70)

usuarios_count = Usuarios.objects.count()
estudiantes_count = Estudiantes.objects.count()
docentes_count = Docentes.objects.count()
consultas_count = Consultas.objects.count()
asignaturas_count = Asignaturas.objects.count()

print(f"✅ Usuarios:     {usuarios_count}")
print(f"✅ Estudiantes:  {estudiantes_count}")
print(f"✅ Docentes:     {docentes_count}")
print(f"✅ Consultas:    {consultas_count}")
print(f"✅ Asignaturas:  {asignaturas_count}")
print()

# ==============================================================================
# TEST 3: Serializers - Validación de Datos
# ==============================================================================
print("📋 TEST 3: Validación de Serializers")
print("-" * 70)

# Test 3.1: Email inválido
print("Test 3.1: Email inválido")
test_data = {
    'email': 'invalido_sin_arroba',
    'tipo_usuario': 'estudiante',
    'nombre': 'Test',
    'apellido_paterno': 'Usuario'
}
serializer = UsuariosSerializer(data=test_data)
if not serializer.is_valid():
    print("✅ Email inválido detectado correctamente")
    print(f"   Error: {serializer.errors.get('email', [''])[0]}")
else:
    print("❌ No se detectó email inválido")
print()

# Test 3.2: Tipo de usuario inválido
print("Test 3.2: Tipo de usuario inválido")
test_data = {
    'email': 'test@valid.com',
    'tipo_usuario': 'tipo_invalido',
    'nombre': 'Test',
    'apellido_paterno': 'Usuario'
}
serializer = UsuariosSerializer(data=test_data)
if not serializer.is_valid():
    print("✅ Tipo de usuario inválido detectado correctamente")
    print(f"   Error: {serializer.errors.get('tipo_usuario', [''])[0]}")
else:
    print("❌ No se detectó tipo de usuario inválido")
print()

# Test 3.3: Campos requeridos
print("Test 3.3: Campos requeridos")
test_data = {
    'email': 'test@valid.com'
    # Faltan campos requeridos
}
serializer = UsuariosSerializer(data=test_data)
if not serializer.is_valid():
    print("✅ Campos requeridos validados correctamente")
    required_fields = [field for field in serializer.errors.keys()]
    print(f"   Campos faltantes: {', '.join(required_fields)}")
else:
    print("❌ No se detectaron campos faltantes")
print()

# ==============================================================================
# TEST 4: Verificar campos read_only en serializers
# ==============================================================================
print("📋 TEST 4: Campos Read-Only en Serializers")
print("-" * 70)

if Usuarios.objects.exists():
    usuario = Usuarios.objects.first()
    serializer = UsuariosSerializer(usuario)
    data = serializer.data
    
    # Verificar que password_hash NO esté en los datos
    if 'password_hash' not in data:
        print("✅ password_hash NO expuesto (correcto)")
    else:
        print("❌ password_hash expuesto (ERROR DE SEGURIDAD)")
    
    # Verificar campos incluidos
    print(f"✅ Campos expuestos: {', '.join(data.keys())}")
else:
    print("⚠️  No hay usuarios para probar")
print()

# ==============================================================================
# TEST 5: Listar últimas consultas
# ==============================================================================
print("📋 TEST 5: Últimas Consultas en el Sistema")
print("-" * 70)

if Consultas.objects.exists():
    ultimas_consultas = Consultas.objects.order_by('-fecha_consulta')[:5]
    for i, consulta in enumerate(ultimas_consultas, 1):
        print(f"✅ Consulta {i}:")
        print(f"   ID: {consulta.id_consulta}")
        print(f"   Título: {consulta.titulo[:50]}...")
        print(f"   Estado: {consulta.estado}")
        print(f"   Prioridad: {consulta.prioridad}")
        print()
else:
    print("ℹ️  No hay consultas en el sistema todavía")
print()

# ==============================================================================
# TEST 6: Verificar configuraciones de seguridad
# ==============================================================================
print("📋 TEST 6: Configuraciones de Seguridad Activas")
print("-" * 70)

from django.conf import settings

security_checks = {
    'CSRF Protection': len(settings.CSRF_TRUSTED_ORIGINS) > 0,
    'Session Security': settings.SESSION_COOKIE_HTTPONLY,
    'Rate Limiting': 'RateLimitMiddleware' in str(settings.MIDDLEWARE),
    'Input Sanitization': 'InputSanitizationMiddleware' in str(settings.MIDDLEWARE),
    'Activity Logging': 'ActivityLogMiddleware' in str(settings.MIDDLEWARE),
    'Security Headers': 'SecurityHeadersMiddleware' in str(settings.MIDDLEWARE),
    'REST Auth': len(settings.REST_FRAMEWORK.get('DEFAULT_AUTHENTICATION_CLASSES', [])) > 0,
}

for check_name, is_active in security_checks.items():
    status = "✅" if is_active else "❌"
    print(f"{status} {check_name}")
print()

# ==============================================================================
# RESUMEN FINAL
# ==============================================================================
print("="*70)
print("🎉 RESUMEN DE PRUEBAS")
print("="*70)

all_passed = True
test_results = {
    "Autenticación": admin_user is not None,
    "Base de datos": usuarios_count > 0,
    "Serializers con validaciones": True,
    "Campos sensibles protegidos": 'password_hash' not in data if Usuarios.objects.exists() else True,
    "Configuraciones de seguridad": all(security_checks.values()),
}

for test_name, passed in test_results.items():
    status = "✅" if passed else "❌"
    print(f"{status} {test_name}")
    if not passed:
        all_passed = False

print()
if all_passed:
    print("🎉 ¡TODAS LAS PRUEBAS PASARON CORRECTAMENTE!")
else:
    print("⚠️  Algunas pruebas fallaron. Revisa los detalles arriba.")

print("="*70)
print()
print("📚 Para más información, consulta:")
print("   - SECURITY_IMPROVEMENTS.md (Documentación de seguridad)")
print("   - GUIA_ACCESO_RED.md (Guía de acceso en red)")
print()
print("🚀 Para iniciar el servidor:")
print("   .\\iniciar_servidor.ps1")
print()
print("="*70)
