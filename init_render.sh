#!/bin/bash
set -e

echo "=== Ejecutando migraciones de Django ==="
python manage.py migrate --no-input
echo "✅ Migraciones completadas"

echo "=== Creando usuarios del sistema ==="
python manage.py shell << 'END'
from django.contrib.auth.models import User
from EduConnectApp.models import Usuarios
from django.utils import timezone

# Crear superusuario admin Django
try:
    if not User.objects.filter(username='admin@example.com').exists():
        User.objects.create_superuser('admin@example.com', 'admin@example.com', 'admin123')
        print("✅ Superusuario Django creado: admin@example.com / admin123")
    else:
        print("✅ Superusuario Django ya existe")
except Exception as e:
    print(f"❌ Error creando admin: {e}")

# Crear estudiante de prueba
try:
    if not Usuarios.objects.filter(email='student1@example.com').exists():
        user = User.objects.create_user(
            username='student1@example.com',
            email='student1@example.com',
            password='studpass'
        )
        
        Usuarios.objects.create(
            email='student1@example.com',
            nombre='Joseph',
            apellido_paterno='Nohra',
            apellido_materno='',
            tipo_usuario='estudiante',
            estado='activo',
            password_hash=user.password,
            telefono='',
            direccion='',
            fecha_creacion=timezone.now(),
            fecha_actualizacion=timezone.now()
        )
        print("✅ Estudiante creado: student1@example.com / studpass")
    else:
        print("✅ Estudiante ya existe")
except Exception as e:
    print(f"❌ Error creando estudiante: {e}")

# Crear docente de prueba
try:
    if not Usuarios.objects.filter(email='docente1@example.com').exists():
        user = User.objects.create_user(
            username='docente1@example.com',
            email='docente1@example.com',
            password='docpass'
        )
        
        Usuarios.objects.create(
            email='docente1@example.com',
            nombre='Sebastian',
            apellido_paterno='Pizarro',
            apellido_materno='',
            tipo_usuario='docente',
            estado='activo',
            password_hash=user.password,
            telefono='',
            direccion='',
            fecha_creacion=timezone.now(),
            fecha_actualizacion=timezone.now()
        )
        print("✅ Docente creado: docente1@example.com / docpass")
    else:
        print("✅ Docente ya existe")
except Exception as e:
    print(f"❌ Error creando docente: {e}")

print("\n✅ ¡Inicialización completada!")
END

echo "=== Inicialización completada ==="
