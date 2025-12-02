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
import time

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

# Check for DATABASE_URL
if not os.environ.get('DATABASE_URL'):
    logger.warning("⚠️  DATABASE_URL not set, waiting for Render to configure it...")
    time.sleep(2)

django.setup()

def wait_for_db(max_attempts=30):
    """Wait for database to be available."""
    from django.db import connection
    from django.db.utils import OperationalError
    
    for attempt in range(max_attempts):
        try:
            connection.ensure_connection()
            logger.info("✅ Database connection successful")
            return True
        except OperationalError as e:
            if attempt < max_attempts - 1:
                logger.info(f"⏳ Database not ready, attempt {attempt + 1}/{max_attempts}, retrying in 2 seconds...")
                time.sleep(2)
            else:
                logger.error(f"❌ Database connection failed after {max_attempts} attempts: {e}")
                return False
    return False

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
    from EduConnectApp.models import Usuarios, Estudiantes, Docentes
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
        student_user_obj = Usuarios.objects.filter(email='student1@example.com').first()
        if not student_user_obj:
            user = User.objects.create_user('student1@example.com', 'student1@example.com', 'studpass')
            student_user_obj = Usuarios.objects.create(
                email='student1@example.com',
                nombre='Joseph',
                apellido_paterno='Nohra',
                apellido_materno='',
                tipo_usuario='estudiante',
                estado='activo',
                password_hash=user.password,
                telefono='',
                fecha_registro=timezone.now(),
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            logger.info("✅ Student Usuarios created: student1@example.com / studpass")
            users_created = True
        else:
            logger.info("✅ Student Usuarios already exists")
        
        # Create Estudiantes profile if not exists
        if not Estudiantes.objects.filter(id_usuario=student_user_obj.id_usuario).exists():
            Estudiantes.objects.create(
                id_usuario=student_user_obj,
                numero_matricula='STU0001',
                carrera='Ingeniería Informática',
                semestre=5,
                fecha_ingreso=timezone.now().date(),
                estado='activo',
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            logger.info("✅ Estudiantes profile created for student1")
        else:
            logger.info("✅ Estudiantes profile already exists for student1")
    except Exception as e:
        logger.warning(f"⚠️  Error creating student: {e}", exc_info=True)
    
    # Create Teacher
    try:
        teacher_user_obj = Usuarios.objects.filter(email='docente1@example.com').first()
        if not teacher_user_obj:
            user = User.objects.create_user('docente1@example.com', 'docente1@example.com', 'docpass')
            teacher_user_obj = Usuarios.objects.create(
                email='docente1@example.com',
                nombre='Sebastian',
                apellido_paterno='Pizarro',
                apellido_materno='',
                tipo_usuario='docente',
                estado='activo',
                password_hash=user.password,
                telefono='',
                fecha_registro=timezone.now(),
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            logger.info("✅ Teacher Usuarios created: docente1@example.com / docpass")
            users_created = True
        else:
            logger.info("✅ Teacher Usuarios already exists")
        
        # Create Docentes profile if not exists
        if not Docentes.objects.filter(id_usuario=teacher_user_obj.id_usuario).exists():
            Docentes.objects.create(
                id_usuario=teacher_user_obj,
                codigo_docente='DOC001',
                departamento='Departamento de Informática',
                titulo_academico='Magister en Ingeniería',
                estado='activo',
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            logger.info("✅ Docentes profile created for docente1")
        else:
            logger.info("✅ Docentes profile already exists for docente1")
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
        
        # Wait for database
        logger.info("Waiting for database connection...")
        if not wait_for_db():
            logger.warning("⚠️  Database connection failed, but continuing with migrations anyway...")
        
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


