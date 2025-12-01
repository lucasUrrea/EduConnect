import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
django.setup()

from EduConnectApp.models import Asignaturas, CategoriasTemas, Usuarios, Docentes, DocenteAsignatura, Consultas, Respuestas, Estudiantes
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone

print('Seeding example data...')

# Crear asignaturas
asig1, _ = Asignaturas.objects.get_or_create(codigo_asignatura='MAT101', defaults={'nombre_asignatura': 'Matemáticas I', 'estado': 'activa'})
asig2, _ = Asignaturas.objects.get_or_create(codigo_asignatura='FIS101', defaults={'nombre_asignatura': 'Física I', 'estado': 'activa'})

# Crear categorias
cat1, _ = CategoriasTemas.objects.get_or_create(id_asignatura=asig1, nombre_categoria='Álgebra', defaults={'estado': 'activa'})
cat2, _ = CategoriasTemas.objects.get_or_create(id_asignatura=asig1, nombre_categoria='Cálculo', defaults={'estado': 'activa'})

# Crear docente
doc_email = 'docente1@example.com'
if not Usuarios.objects.filter(email=doc_email).exists():
    u_doc = Usuarios.objects.create(email=doc_email, password_hash=make_password('DocPass123!'), tipo_usuario='docente', nombre='Docente', apellido_paterno='Uno', estado='activo')
    User.objects.get_or_create(username=doc_email, defaults={'email': doc_email, 'first_name': 'Docente', 'last_name': 'Uno'})
    docente = Docentes.objects.create(id_usuario=u_doc, codigo_docente='DOC001')
    DocenteAsignatura.objects.create(id_docente=docente, id_asignatura=asig1, periodo_academico='2025-1', grupo='A')
else:
    docente = Docentes.objects.filter(id_usuario__email=doc_email).first()

# Crear estudiante
stu_email = 'student1@example.com'
if not Usuarios.objects.filter(email=stu_email).exists():
    u_stu = Usuarios.objects.create(email=stu_email, password_hash=make_password('StudPass123!'), tipo_usuario='estudiante', nombre='Student', apellido_paterno='Uno', estado='activo')
    django_user, _ = User.objects.get_or_create(username=stu_email, defaults={'email': stu_email, 'first_name': 'Student', 'last_name': 'Uno'})
    django_user.set_password('StudPass123!')
    django_user.save()
    estudiante = Estudiantes.objects.create(id_usuario=u_stu, numero_matricula='STU0001')
else:
    estudiante = Estudiantes.objects.filter(id_usuario__email=stu_email).first()

# Crear una consulta y respuesta
consulta = Consultas.objects.create(id_estudiante=estudiante, id_asignatura=asig1, titulo='¿Cómo resolver esta integral?', descripcion='Necesito ayuda con la integral por partes', fecha_consulta=timezone.now(), estado='pendiente')
respuesta = Respuestas.objects.create(id_consulta=consulta, id_docente=docente, contenido_respuesta='Intenta usar u=... dv=...', fecha_respuesta=timezone.now(), tiempo_respuesta_horas=2)

print('Seeding complete')
