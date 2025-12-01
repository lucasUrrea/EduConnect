#!/usr/bin/env python
"""
Script para crear un usuario administrador con acceso web
"""
import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
os.environ['USE_SQLITE'] = '1'
django.setup()

from EduConnectApp.models import Usuarios

print("="*70)
print("👑 CREANDO USUARIO ADMINISTRADOR WEB")
print("="*70)
print()

# Datos del administrador
admin_email = "admin@educonnect.com"
admin_password = "admin123"

# Verificar si ya existe
try:
    admin = Usuarios.objects.get(email=admin_email)
    print(f"⚠️  El usuario {admin_email} ya existe.")
    print(f"   Actualizando contraseña...")
    admin.password_hash = make_password(admin_password)
    admin.tipo_usuario = 'administrador'
    admin.estado = 'activo'
    admin.save()
    print(f"✅ Contraseña actualizada")
except Usuarios.DoesNotExist:
    # Crear nuevo administrador
    admin = Usuarios.objects.create(
        email=admin_email,
        password_hash=make_password(admin_password),
        nombre="Admin",
        apellido_paterno="Sistema",
        apellido_materno="EduConnect",
        tipo_usuario='administrador',
        estado='activo'
    )
    print(f"✅ Usuario administrador creado exitosamente")

print()
print("="*70)
print("📋 CREDENCIALES DEL ADMINISTRADOR WEB")
print("="*70)
print(f"\n📧 Email:    {admin_email}")
print(f"🔑 Password: {admin_password}")
print(f"👤 Tipo:     Administrador")
print(f"✅ Estado:   Activo")
print()
print("🌐 URLs de acceso:")
print(f"   - Login: http://localhost:8000/login/")
print(f"   - Red:   http://10.58.0.197:8000/login/")
print()
print("="*70)
print("✅ ¡Listo! Puedes usar estas credenciales para acceder")
print("="*70)
