#!/bin/bash
set -e

echo "=== INSTALANDO DEPENDENCIAS ==="
pip install -r requirements.txt

echo "=== EJECUTANDO MIGRACIONES ==="
python manage.py migrate --no-input

echo "=== RECOPILANDO ARCHIVOS ESTÁTICOS ==="
python manage.py collectstatic --no-input --clear

echo "=== CREANDO USUARIOS INICIALES ==="
python manage.py shell << 'ENDSHELL'
from django.contrib.auth.models import User
from EduConnectApp.models import Usuarios
from django.utils import timezone

try:
    if not User.objects.filter(username='admin@example.com').exists():
        User.objects.create_superuser('admin@example.com', 'admin@example.com', 'admin123')
        print("Admin creado")
except Exception as e:
    print(f"Admin error: {e}")

try:
    if not Usuarios.objects.filter(email='student1@example.com').exists():
        user = User.objects.create_user('student1@example.com', 'student1@example.com', 'studpass')
        Usuarios.objects.create(
            email='student1@example.com', nombre='Joseph', apellido_paterno='Nohra',
            apellido_materno='', tipo_usuario='estudiante', estado='activo',
            password_hash=user.password, telefono='', direccion='',
            fecha_creacion=timezone.now(), fecha_actualizacion=timezone.now()
        )
        print("Estudiante creado")
except Exception as e:
    print(f"Estudiante error: {e}")

try:
    if not Usuarios.objects.filter(email='docente1@example.com').exists():
        user = User.objects.create_user('docente1@example.com', 'docente1@example.com', 'docpass')
        Usuarios.objects.create(
            email='docente1@example.com', nombre='Sebastian', apellido_paterno='Pizarro',
            apellido_materno='', tipo_usuario='docente', estado='activo',
            password_hash=user.password, telefono='', direccion='',
            fecha_creacion=timezone.now(), fecha_actualizacion=timezone.now()
        )
        print("Docente creado")
except Exception as e:
    print(f"Docente error: {e}")

print("Inicializacion completada!")
ENDSHELL

echo "=== BUILD EXITOSO ==="