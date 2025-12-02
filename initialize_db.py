"""
Script de inicialización de la base de datos para Render.
Se ejecuta una sola vez al iniciar la aplicación.
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
django.setup()

from django.contrib.auth.models import User
from EduConnectApp.models import Usuarios
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def initialize_database():
    """Inicializar la base de datos con migraciones y usuarios."""
    
    try:
        # Ejecutar migraciones
        from django.core.management import call_command
        print("=== Ejecutando migraciones ===")
        call_command('migrate', '--no-input', verbosity=1)
        print("✅ Migraciones completadas")
    except Exception as e:
        print(f"❌ Error en migraciones: {e}")
        return False

    try:
        # Crear superusuario admin
        print("\n=== Creando usuarios ===")
        if not User.objects.filter(username='admin@example.com').exists():
            User.objects.create_superuser('admin@example.com', 'admin@example.com', 'admin123')
            print("✅ Admin creado: admin@example.com / admin123")
        else:
            print("✅ Admin ya existe")
    except Exception as e:
        print(f"⚠️ Error en admin: {e}")

    try:
        # Crear estudiante
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
            print("✅ Estudiante creado: student1@example.com / studpass")
        else:
            print("✅ Estudiante ya existe")
    except Exception as e:
        print(f"⚠️ Error en estudiante: {e}")

    try:
        # Crear docente
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
            print("✅ Docente creado: docente1@example.com / docpass")
        else:
            print("✅ Docente ya existe")
    except Exception as e:
        print(f"⚠️ Error en docente: {e}")

    print("\n✅ Inicialización completada!")
    return True

if __name__ == '__main__':
    # Solo ejecutar en producción (cuando DATABASE_URL esté set)
    if os.environ.get('DATABASE_URL'):
        print("\n=== RENDER INITIALIZATION ===")
        initialize_database()
    else:
        print("DATABASE_URL no configurada. Omitiendo inicialización.")
