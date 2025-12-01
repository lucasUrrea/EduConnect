import os, sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
import django
from django.utils import timezone

django.setup()
from EduConnectApp.models import Asignaturas, CategoriasTemas, Estudiantes, Consultas, DocenteAsignatura, Docentes

print('Adding asignaturas, categorias, and two consultas...')

# Add asignaturas
new_asigs = [
    ('ENG101','Ingeniería de Software I'),
    ('DB101','Bases de Datos I'),
    ('ALGO101','Algoritmos I'),
]
created_asigs = []
for code, name in new_asigs:
    a, created = Asignaturas.objects.get_or_create(codigo_asignatura=code, defaults={'nombre_asignatura': name, 'estado':'activa'})
    created_asigs.append(a)
    print('Asignatura:', a.id_asignatura, a.nombre_asignatura, 'created?' , created)

# Add categorias for first new asignatura
a0 = created_asigs[0]
cats = ['General','Tareas','Exámenes']
created_cats = []
for c in cats:
    cat, created = CategoriasTemas.objects.get_or_create(id_asignatura=a0, nombre_categoria=c, defaults={'estado':'activa'})
    created_cats.append(cat)
    print('Categoria:', cat.id_categoria, cat.nombre_categoria, 'created?', created)

# Choose two estudiantes to attach consultas to
students = list(Estudiantes.objects.all()[:5])
if len(students) < 2:
    print('No hay suficientes estudiantes para crear consultas. Abortando.')
    sys.exit(1)

est1 = students[0]
est2 = students[1]

# Find an asignatura that has a docente assigned (for richness)
doc_asig = DocenteAsignatura.objects.select_related('id_docente','id_asignatura').first()
if doc_asig:
    asign_for_consulta = doc_asig.id_asignatura
else:
    asign_for_consulta = created_asigs[1]

# Create two consultas
c1, c1_created = Consultas.objects.get_or_create(
    titulo='Consulta generada en vivo: duda sobre entregables',
    defaults={
        'id_estudiante': est1,
        'id_asignatura': asign_for_consulta,
        'id_categoria': created_cats[0] if created_cats else None,
        'descripcion': 'Tengo dudas sobre el alcance del entregable 2.',
        'fecha_consulta': timezone.now(),
        'estado': 'pendiente'
    }
)
print('Consulta1:', c1.id_consulta, 'created?', c1_created)

c2, c2_created = Consultas.objects.get_or_create(
    titulo='Consulta generada en vivo: problema en SQL JOIN',
    defaults={
        'id_estudiante': est2,
        'id_asignatura': asign_for_consulta,
        'id_categoria': created_cats[1] if len(created_cats)>1 else None,
        'descripcion': 'No logro obtener los resultados esperados con JOINs múltiples.',
        'fecha_consulta': timezone.now(),
        'estado': 'pendiente'
    }
)
print('Consulta2:', c2.id_consulta, 'created?', c2_created)

# Summary counts
print('\nSummary after additions:')
from EduConnectApp.models import Usuarios, Docentes, Estudiantes, Asignaturas, Consultas, Respuestas, CategoriasTemas
print('Usuarios:', Usuarios.objects.count())
print('Docentes:', Docentes.objects.count())
print('Estudiantes:', Estudiantes.objects.count())
print('Asignaturas:', Asignaturas.objects.count())
print('Categorias:', CategoriasTemas.objects.count())
print('Consultas:', Consultas.objects.count())
print('Respuestas:', Respuestas.objects.count())

print('\nLatest created consultas:')
for c in Consultas.objects.order_by('-fecha_consulta')[:10]:
    print(c.id_consulta, c.titulo, c.id_estudiante.id_estudiante, c.id_asignatura.nombre_asignatura, c.id_categoria.nombre_categoria if c.id_categoria else 'N/A', c.estado)

print('Done.')
