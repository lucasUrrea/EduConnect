import os,sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
sys.path.insert(0, os.getcwd())
import django
django.setup()
from EduConnectApp.models import Consultas
from django.test import Client

qs = Consultas.objects.all()
print('consultas count=', qs.count())
if qs.exists():
    print('first id=', qs.first().id_consulta)
    c=Client()
    print('anon GET /consulta/%s/ ->' % qs.first().id_consulta, c.get(f'/consulta/{qs.first().id_consulta}/').status_code)
else:
    print('no consultas found')
