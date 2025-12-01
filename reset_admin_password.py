#!/usr/bin/env python
"""
Script para resetear la contraseña del superusuario admin
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
os.environ['USE_SQLITE'] = '1'
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Buscar o crear el usuario admin
username = 'admin'
email = 'admin@admin.com'
password = 'admin123'

try:
    user = User.objects.get(username=username)
    print(f"Usuario '{username}' encontrado. Actualizando...")
    user.email = email
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print("✓ Contraseña actualizada exitosamente!")
except User.DoesNotExist:
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("✓ Nuevo superusuario creado exitosamente!")

print("\n" + "="*50)
print("CREDENCIALES DE ACCESO:")
print("="*50)
print(f"Usuario:     {username}")
print(f"Contraseña:  {password}")
print(f"Email:       {email}")
print("="*50)
print("\nAccede en: http://localhost:8000/admin/")
print("="*50)
