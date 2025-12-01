#!/usr/bin/env python
"""
Script para resetear o crear el usuario admin con credenciales conocidas
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
os.environ['USE_SQLITE'] = '1'
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Credenciales simples
USERNAME = 'admin'
EMAIL = 'admin@admin.com'
PASSWORD = 'admin123'

try:
    # Intentar obtener el usuario existente
    user = User.objects.get(username=USERNAME)
    print(f"✓ Usuario '{USERNAME}' ya existe. Actualizando contraseña...")
    user.set_password(PASSWORD)
    user.email = EMAIL
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"✓ Contraseña actualizada exitosamente")
except User.DoesNotExist:
    # Crear nuevo usuario
    print(f"Creando nuevo superusuario '{USERNAME}'...")
    user = User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print(f"✓ Superusuario creado exitosamente")

print("\n" + "="*50)
print("CREDENCIALES DE ACCESO")
print("="*50)
print(f"Usuario:    {USERNAME}")
print(f"Email:      {EMAIL}")
print(f"Contraseña: {PASSWORD}")
print("="*50)
print("\nURLs de acceso:")
print("  - http://localhost:8000/admin/")
print("  - http://192.168.1.13:8000/admin/")
print("="*50)
