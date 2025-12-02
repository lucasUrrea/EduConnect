#!/bin/bash
set -e

echo "=========================================="
echo "STARTING DJANGO APPLICATION ON RENDER"
echo "=========================================="

echo ""
echo "=== Step 1: Running Migrations ==="
python manage.py migrate --no-input 2>&1

echo ""
echo "=== Step 2: Creating Initial Users ==="
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
from EduConnectApp.models import Usuarios
from django.utils import timezone
import sys

try:
    if not User.objects.filter(username='admin@example.com').exists():
        User.objects.create_superuser('admin@example.com', 'admin@example.com', 'admin123')
        print("✅ Admin user created: admin@example.com / admin123")
    else:
        print("✅ Admin user already exists")
except Exception as e:
    print(f"⚠️ Error creating admin: {e}")
    sys.exit(1)

try:
    if not Usuarios.objects.filter(email='student1@example.com').exists():
        user = User.objects.create_user('student1@example.com', 'student1@example.com', 'studpass')
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
        print("✅ Student user created: student1@example.com / studpass")
    else:
        print("✅ Student user already exists")
except Exception as e:
    print(f"⚠️ Error creating student: {e}")
    sys.exit(1)

try:
    if not Usuarios.objects.filter(email='docente1@example.com').exists():
        user = User.objects.create_user('docente1@example.com', 'docente1@example.com', 'docpass')
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
        print("✅ Teacher user created: docente1@example.com / docpass")
    else:
        print("✅ Teacher user already exists")
except Exception as e:
    print(f"⚠️ Error creating teacher: {e}")
    sys.exit(1)

print("\n✅ Database initialization completed successfully!")
EOF

echo ""
echo "=== Step 3: Starting Gunicorn Server ==="
echo "Listening on 0.0.0.0:10000"
exec gunicorn modulos_consultas.wsgi:application --bind 0.0.0.0:10000 --workers 2 --timeout 120 --access-logfile - --error-logfile -
