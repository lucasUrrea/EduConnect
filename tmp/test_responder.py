import os, sys, django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
# ensure project root is on sys.path
sys.path.insert(0, os.getcwd())

try:
    django.setup()
except Exception as e:
    print('Django setup error:', e)
    raise

from django.test import Client
from EduConnectApp.models import Usuarios, Docentes, Estudiantes, Consultas, Respuestas

c = Client()

# find a docente and a pending consulta
usuario_doc = Usuarios.objects.filter(tipo_usuario='docente').first()
if usuario_doc:
    docente = Docentes.objects.filter(id_usuario=usuario_doc).first()
else:
    docente = None

print('Found usuario_doc:', getattr(usuario_doc, 'id_usuario', None))
print('Found docente:', getattr(docente, 'id_docente', None))

consulta = Consultas.objects.filter(estado='pendiente').first()
if not consulta:
    estudiante_usuario = Usuarios.objects.filter(tipo_usuario='estudiante').first()
    if estudiante_usuario:
        estudiante = Estudiantes.objects.filter(id_usuario=estudiante_usuario.id_usuario).first()
    else:
        estudiante = None
    if estudiante:
        consulta = Consultas(
            id_estudiante=estudiante,
            id_asignatura=None,
            titulo='Test pendiente',
            descripcion='Texto de prueba',
            fecha_consulta=timezone.now(),
            estado='pendiente'
        )
        consulta.save()
        print('Created consulta', consulta.id_consulta)
    else:
        print('No estudiante available; aborting')
        sys.exit(0)

# require a docente to proceed
if not docente:
    print('No docente available; aborting')
    sys.exit(0)

# set session as docente
session = c.session
# docente.id_usuario is a Usuarios instance; its PK is id_usuario
session['usuario_id'] = docente.id_usuario.id_usuario
session['tipo_usuario'] = 'docente'
session.save()

# Post response
resp = c.post(f'/consulta/{consulta.id_consulta}/responder/', {'contenido_respuesta': 'Respuesta de prueba desde test client'})
print('POST status_code=', resp.status_code)
print('POST content (truncated):')
print(resp.content.decode('utf-8')[:2000])

# show possible saved respuesta
r = Respuestas.objects.filter(id_consulta=consulta).order_by('-id_respuesta').first()
print('Latest respuesta for consulta:', getattr(r,'id_respuesta',None), getattr(r,'contenido_respuesta',None))

# show consulta estado
consulta.refresh_from_db()
print('Consulta estado after POST:', consulta.estado)
