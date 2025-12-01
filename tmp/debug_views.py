import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
sys.path.insert(0, os.getcwd())
import django
django.setup()
from django.test import Client
from EduConnectApp.models import Usuarios, Docentes, Estudiantes

c = Client()

def try_get(path, client, label):
    try:
        resp = client.get(path)
        print(f"{label} GET {path} -> status {resp.status_code}")
        print(resp.content.decode('utf-8')[:1000])
    except Exception as e:
        import traceback
        print(f"{label} EXCEPTION for {path}:")
        traceback.print_exc()

# 1) unauthenticated requests
try_get('/consulta/5/', c, 'anon')
try_get('/mi-progreso/', c, 'anon')

# 2) as docente
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
    try_get('/consulta/5/', c2, 'docente')
    try_get('/consulta/5/responder/', c2, 'docente')
else:
    print('no docente found')

# 3) as estudiante
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
    try_get('/mi-progreso/', c3, 'estudiante')
else:
    print('no estudiante found')
