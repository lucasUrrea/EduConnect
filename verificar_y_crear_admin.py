#!/usr/bin/env python
"""
Script para verificar y crear/actualizar el superusuario admin
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
os.environ['USE_SQLITE'] = '1'
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("="*60)
print("VERIFICANDO USUARIOS EN LA BASE DE DATOS")
print("="*60)

# Listar todos los usuarios
all_users = User.objects.all()
print(f"\nTotal de usuarios: {all_users.count()}")
for user in all_users:
    print(f"\n- Usuario: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Es superusuario: {user.is_superuser}")
    print(f"  Es staff: {user.is_staff}")
    print(f"  Activo: {user.is_active}")

print("\n" + "="*60)
print("RECREANDO SUPERUSUARIO ADMIN")
print("="*60)

# Eliminar usuario admin si existe
User.objects.filter(username='admin').delete()
print("\n✓ Usuario anterior eliminado (si existía)")

# Crear nuevo superusuario
username = 'admin'
password = 'admin123'
email = 'admin@admin.com'

user = User.objects.create_superuser(
    username=username,
    email=email,
    password=password
)

print("✓ Nuevo superusuario creado exitosamente!")

# Verificar que se creó correctamente
user_check = User.objects.get(username=username)
print(f"\nVerificación:")
print(f"  Username: {user_check.username}")
print(f"  Email: {user_check.email}")
print(f"  Is superuser: {user_check.is_superuser}")
print(f"  Is staff: {user_check.is_staff}")
print(f"  Is active: {user_check.is_active}")
print(f"  Tiene contraseña válida: {user_check.password.startswith('pbkdf2_')}")

# Probar autenticación
from django.contrib.auth import authenticate
test_user = authenticate(username=username, password=password)
if test_user:
    print(f"\n✓✓ AUTENTICACIÓN EXITOSA ✓✓")
else:
    print(f"\n✗✗ ERROR EN AUTENTICACIÓN ✗✗")

print("\n" + "="*60)
print("CREDENCIALES DE ACCESO:")
print("="*60)
print(f"Usuario:     {username}")
print(f"Contraseña:  {password}")
print(f"Email:       {email}")
print("="*60)
print("\nURL Admin: http://localhost:8000/admin/")
print("="*60)
