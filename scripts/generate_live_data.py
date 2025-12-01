import os, sys, random, datetime
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
import django
from django.utils import timezone

django.setup()
from EduConnectApp.models import Usuarios, Estudiantes, Docentes, Asignaturas, DocenteAsignatura, Consultas, Respuestas
from django.contrib.auth.models import User

print('Generating live data...')

# Ensure some asignaturas exist
asig_names = [
    ('MAT201','Matemáticas II'),
    ('FIS201','Física II'),
    ('PROG101','Programación I'),
    ('STA101','Estadística I'),
]
asignaturas = []
for code,name in asig_names:
    a, created = Asignaturas.objects.get_or_create(codigo_asignatura=code, defaults={'nombre_asignatura': name, 'estado':'activa'})
    asignaturas.append(a)

# Create docentes (if not exist)
docente_users = []
for i in range(1,4):
    email = f'doc_live{i}@example.com'
    u, created = Usuarios.objects.get_or_create(email=email, defaults={'password_hash':'pbkdf2_sha256$1000000$test$hash','tipo_usuario':'docente','nombre':f'Doc{i}','apellido_paterno':'Live','estado':'activo'})
    du, duc = User.objects.get_or_create(username=email, defaults={'email':email,'first_name':u.nombre})
    if duc:
        du.set_password('docpass')
        du.save()
    d, dc = Docentes.objects.get_or_create(id_usuario=u, defaults={'codigo_docente': f'DOCLIVE{i}'})
    docente_users.append(d)

# Assign docentes to asignaturas
for idx, d in enumerate(docente_users):
    a = asignaturas[idx % len(asignaturas)]
    DocenteAsignatura.objects.get_or_create(id_docente=d, id_asignatura=a, defaults={'periodo_academico':'2025-1','grupo':'A'})

# Create estudiantes and consultas
for i in range(1,11):
    email = f'stud_live{i}@example.com'
    user, created = Usuarios.objects.get_or_create(email=email, defaults={'password_hash':'pbkdf2_sha256$1000000$test$hash','tipo_usuario':'estudiante','nombre':f'Student{i}','apellido_paterno':'Live','estado':'activo'})
    django_u, duc = User.objects.get_or_create(username=email, defaults={'email':email,'first_name':user.nombre})
    if duc:
        django_u.set_password('studpass')
        django_u.save()
    est, esc = Estudiantes.objects.get_or_create(id_usuario=user, defaults={'numero_matricula':f'LM{i:04d}'})
    # each student creates 1-3 consultas
    for j in range(random.randint(1,3)):
        a = random.choice(asignaturas)
        titulo = f'Consulta live {i}-{j} sobre {a.nombre_asignatura}'
        fecha = timezone.now() - datetime.timedelta(days=random.randint(0,30), hours=random.randint(0,23))
        consulta, created = Consultas.objects.get_or_create(titulo=titulo, defaults={
            'id_estudiante': est,
            'id_asignatura': a,
            'descripcion': f'Descripción automática {i}-{j}',
            'fecha_consulta': fecha,
            'estado': random.choice(['pendiente','respondida'])
        })
        # optionally create a respuesta if estado is respondida
        if consulta.estado == 'respondida':
            # choose a docente assigned to this asignatura
            das = DocenteAsignatura.objects.filter(id_asignatura=a)
            if das.exists():
                doc = das.order_by('?').first().id_docente
                Respuestas.objects.get_or_create(id_consulta=consulta, defaults={
                    'id_docente': doc,
                    'contenido_respuesta': 'Respuesta automática generada',
                    'fecha_respuesta': consulta.fecha_consulta + datetime.timedelta(hours=random.randint(1,72)),
                    'tiempo_respuesta_horas': random.randint(1,72)
                })

# summary
print('Summary counts after generation:')
print('Usuarios:', Usuarios.objects.count())
print('Docentes:', Docentes.objects.count())
print('Estudiantes:', Estudiantes.objects.count())
print('Asignaturas:', Asignaturas.objects.count())
print('Consultas:', Consultas.objects.count())
print('Respuestas:', Respuestas.objects.count())

# show 10 latest consultas
for c in Consultas.objects.order_by('-fecha_consulta')[:10]:
    print(c.id_consulta, c.titulo, c.estado, c.fecha_consulta, 'estudiante->usuario', c.id_estudiante.id_usuario_id)

print('Done.')
