import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
sys.path.insert(0, os.getcwd())
import django
django.setup()
from django.test import Client
from EduConnectApp.models import Usuarios, Docentes, Estudiantes

c = Client()
print('anon GET / ->', c.get('/').status_code)
print('anon GET /login/ ->', c.get('/login/').status_code)
print('anon GET /mi-progreso/ ->', c.get('/mi-progreso/').status_code)

usuario_doc = Usuarios.objects.filter(tipo_usuario='docente').first()
if usuario_doc:
    docente = Docentes.objects.filter(id_usuario=usuario_doc.id_usuario).first()
else:
    docente = None

if docente:
    c2 = Client()
    s = c2.session
    s['usuario_id'] = docente.id_usuario.id_usuario
    s['tipo_usuario'] = 'docente'
    s.save()
    print('docente GET /consulta/5/ ->', c2.get('/consulta/5/').status_code)
    print('docente GET /consulta/5/responder/ ->', c2.get(f'/consulta/5/responder/').status_code)
else:
    print('no docente found')

usuario_est = Usuarios.objects.filter(tipo_usuario='estudiante').first()
if usuario_est:
    estudiante = Estudiantes.objects.filter(id_usuario=usuario_est.id_usuario).first()
else:
    estudiante = None

if estudiante:
    c3 = Client()
    s = c3.session
    s['usuario_id'] = estudiante.id_usuario.id_usuario
    s['tipo_usuario'] = 'estudiante'
    s.save()
    print('estudiante GET /mi-progreso/ ->', c3.get('/mi-progreso/').status_code)
else:
    print('no estudiante found')
