import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
sys.path.insert(0, os.getcwd())
import django
django.setup()
from django.test import Client

c = Client()
pk = 5
try:
    resp = c.get(f'/consulta/{pk}/')
    print('Status:', resp.status_code)
    print('Content snippet:')
    print(resp.content.decode('utf-8')[:1000])
except Exception as e:
    import traceback
    traceback.print_exc()
    print('Exception:', e)
