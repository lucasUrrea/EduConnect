import os
import sys
import django
import pathlib

proj_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(proj_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
django.setup()

from django.test import Client
from EduConnectApp.models import Estudiantes, Consultas
from django.core.files.uploadedfile import SimpleUploadedFile

c = Client()
est = Estudiantes.objects.first()
if not est:
    print('No estudiantes found')
    sys.exit(1)

# login or session
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.filter(username=est.id_usuario.email).first()
if u:
    c.force_login(u)
else:
    s = c.session
    s['usuario_id'] = est.id_usuario.id_usuario
    s['tipo_usuario'] = 'estudiante'
    s['nombre_completo'] = est.id_usuario.nombre + ' ' + est.id_usuario.apellido_paterno
    s.save()

before = Consultas.objects.count()
print('Consultas before:', before)

file_content = b'This is a test attachment for create consulta script.'
up = SimpleUploadedFile('test.txt', file_content, content_type='text/plain')

post_data = {
    'id_asignatura': '1',
    'id_categoria': '',
    'titulo': 'Prueba creación automática',
    'descripcion': 'Esta es una consulta generada por script para probar la creación desde el cliente de pruebas.',
    'prioridad': 'media',
    'tipo_consulta': 'consulta_general',
    'es_anonima': 'on',
}
post_data['adjunto_archivo'] = up

# Send without follow to observe initial response and ensure FILES is processed
resp = c.post('/consulta/crear/', data=post_data)
print('POST status_code:', resp.status_code)

after = Consultas.objects.count()
print('Consultas after:', after)
if after > before:
    new = Consultas.objects.order_by('-id_consulta').first()
    print('Created consulta id=', new.id_consulta, 'titulo=', new.titulo)
else:
    print('No new consulta was created; response content length:', len(resp.content))
    # dump small portion of response for debugging
    print(resp.content.decode('utf-8')[:800])
