#!/usr/bin/env python
"""
Startup script for Render deployment.
Executes migrations, creates initial users, and starts Gunicorn.
"""
import os
import sys
import subprocess
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
django.setup()

def run_migrations():
    """Execute database migrations."""
    print("\n" + "="*60)
    print("STEP 1: Running Database Migrations")
    print("="*60)
    try:
        from django.core.management import call_command
        call_command('migrate', '--no-input', verbosity=1)
        print("✅ Migrations completed successfully")
        return True
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False

def create_users():
    """Create initial users for testing."""
    print("\n" + "="*60)
    print("STEP 2: Creating Initial Users")
    print("="*60)
    
    from django.contrib.auth.models import User
    from EduConnectApp.models import Usuarios
    from django.utils import timezone
    
    users_created = False
    
    # Create Admin
    try:
        if not User.objects.filter(username='admin@example.com').exists():
            User.objects.create_superuser('admin@example.com', 'admin@example.com', 'admin123')
            print("✅ Admin user created: admin@example.com / admin123")
            users_created = True
        else:
            print("✅ Admin user already exists")
    except Exception as e:
        print(f"⚠️  Error creating admin: {e}")
    
    # Create Student
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
            users_created = True
        else:
            print("✅ Student user already exists")
    except Exception as e:
        print(f"⚠️  Error creating student: {e}")
    
    # Create Teacher
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
            users_created = True
        else:
            print("✅ Teacher user already exists")
    except Exception as e:
        print(f"⚠️  Error creating teacher: {e}")
    
    return users_created

def start_gunicorn():
    """Start Gunicorn server."""
    print("\n" + "="*60)
    print("STEP 3: Starting Gunicorn Server")
    print("="*60)
    
    port = os.environ.get('PORT', '10000')
    workers = int(os.environ.get('GUNICORN_WORKERS', '2'))
    timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))
    
    cmd = [
        'gunicorn',
        'modulos_consultas.wsgi:application',
        '--bind', f'0.0.0.0:{port}',
        '--workers', str(workers),
        '--timeout', str(timeout),
        '--access-logfile', '-',
        '--error-logfile', '-'
    ]
    
    print(f"Starting: {' '.join(cmd)}")
    print("="*60 + "\n")
    
    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print("\nShutdown requested")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting Gunicorn: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        # Run all steps
        if not run_migrations():
            print("\n⚠️  Warning: Migrations had issues, continuing anyway...")
        
        create_users()
        start_gunicorn()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
