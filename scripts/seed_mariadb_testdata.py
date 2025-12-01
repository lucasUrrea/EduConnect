import os, sys, datetime
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
import django
from django.utils import timezone

django.setup()
from EduConnectApp.models import Usuarios, Estudiantes, Consultas, Asignaturas

# Create 2 test usuarios and students, 1 asignatura and 2 consultas

def safe_get_or_create_user(email, nombre='Test', apellido='User', tipo='estudiante'):
    u, created = Usuarios.objects.get_or_create(email=email, defaults={
        'password_hash': 'pbkdf2_sha256$1000000$test$hash',
        'tipo_usuario': tipo,
        'nombre': nombre,
        'apellido_paterno': apellido,
        'estado': 'activo'
    })
    return u, created

print('Seeding test data into MariaDB...')
# Asignatura
asig, _ = Asignaturas.objects.get_or_create(codigo_asignatura='TEST101', defaults={'nombre_asignatura':'Test Asignatura'})
print('Asignatura:', asig.pk, asig.codigo_asignatura)

# Users and estudiantes
u1, c1 = safe_get_or_create_user('seed_student1@example.com', 'Seed', 'Student1', tipo='estudiante')
u2, c2 = safe_get_or_create_user('seed_student2@example.com', 'Seed', 'Student2', tipo='estudiante')
print('Usuarios created:', c1, c2)

# Ensure Estudiantes rows
est1, e1 = Estudiantes.objects.get_or_create(id_usuario=u1, defaults={'numero_matricula':'S1001'})
est2, e2 = Estudiantes.objects.get_or_create(id_usuario=u2, defaults={'numero_matricula':'S1002'})
print('Estudiantes created:', e1, e2)

# Create two consultas
cA, aA = Consultas.objects.get_or_create(
    titulo='Consulta de prueba A',
    defaults={'id_estudiante': est1, 'id_asignatura': asig, 'descripcion':'Esta es una consulta de prueba A', 'fecha_consulta': timezone.now(), 'estado':'pendiente'}
)
cB, aB = Consultas.objects.get_or_create(
    titulo='Consulta de prueba B',
    defaults={'id_estudiante': est2, 'id_asignatura': asig, 'descripcion':'Esta es una consulta de prueba B', 'fecha_consulta': timezone.now(), 'estado':'pendiente'}
)
print('Consultas created:', cA.pk, cB.pk)

# Summary counts
print('\nSummary:')
print('Usuarios count:', Usuarios.objects.count())
print('Estudiantes count:', Estudiantes.objects.count())
print('Asignaturas count:', Asignaturas.objects.count())
print('Consultas count:', Consultas.objects.count())

print('\nDone seeding test data.')
