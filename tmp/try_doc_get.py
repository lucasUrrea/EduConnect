import os,sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
sys.path.insert(0, os.getcwd())
import django
django.setup()
from EduConnectApp.models import Usuarios, Docentes
from django.test import Client

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
    print('docente GET /consulta/1/ ->', c2.get('/consulta/1/').status_code)
else:
    print('no docente found')
