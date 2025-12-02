#!/usr/bin/env python
"""
Startup script for Render deployment.
Executes migrations, creates initial users, and starts Gunicorn.
"""
import os
import sys
import subprocess
import django
import logging

# Setup logging to see output in Render logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger(__name__)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
django.setup()

def run_migrations():
    """Execute database migrations."""
    logger.info("="*60)
    logger.info("STEP 1: Running Database Migrations")
    logger.info("="*60)
    try:
        from django.core.management import call_command
        call_command('migrate', '--no-input', verbosity=2)
        logger.info("✅ Migrations completed successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Migration error: {e}", exc_info=True)
        return False

def create_users():
    """Create initial users for testing."""
    logger.info("="*60)
    logger.info("STEP 2: Creating Initial Users")
    logger.info("="*60)
    
    from django.contrib.auth.models import User
    from EduConnectApp.models import Usuarios
    from django.utils import timezone
    
    users_created = False
    
    # Create Admin
    try:
        if not User.objects.filter(username='admin@example.com').exists():
            User.objects.create_superuser('admin@example.com', 'admin@example.com', 'admin123')
            logger.info("✅ Admin user created: admin@example.com / admin123")
            users_created = True
        else:
            logger.info("✅ Admin user already exists")
    except Exception as e:
        logger.warning(f"⚠️  Error creating admin: {e}", exc_info=True)
    
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
            logger.info("✅ Student user created: student1@example.com / studpass")
            users_created = True
        else:
            logger.info("✅ Student user already exists")
    except Exception as e:
        logger.warning(f"⚠️  Error creating student: {e}", exc_info=True)
    
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
            logger.info("✅ Teacher user created: docente1@example.com / docpass")
            users_created = True
        else:
            logger.info("✅ Teacher user already exists")
    except Exception as e:
        logger.warning(f"⚠️  Error creating teacher: {e}", exc_info=True)
    
    return users_created

def start_gunicorn():
    """Start Gunicorn server."""
    logger.info("="*60)
    logger.info("STEP 3: Starting Gunicorn Server")
    logger.info("="*60)
    
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
    
    logger.info(f"Starting: {' '.join(cmd)}")
    logger.info("="*60)
    
    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error starting Gunicorn: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    try:
        logger.info("╔" + "="*58 + "╗")
        logger.info("║" + " "*58 + "║")
        logger.info("║" + "EDUCONNECT STARTUP SEQUENCE".center(58) + "║")
        logger.info("║" + " "*58 + "║")
        logger.info("╚" + "="*58 + "╝")
        logger.info("")
        
        # Run all steps
        if not run_migrations():
            logger.warning("⚠️  Warning: Migrations had issues, continuing anyway...")
        
        logger.info("")
        create_users()
        
        logger.info("")
        start_gunicorn()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)

