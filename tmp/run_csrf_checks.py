import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
sys.path.insert(0, os.getcwd())
import django
django.setup()
from django.test import Client

c = Client()
print('GET /login/ ->', c.get('/login/').status_code)
print('Cookie after GET /login/:', c.cookies.get('csrftoken'))
print('POST /login/ ->', c.post('/login/', {'email':'nope@example.com', 'password':'x'}).status_code)

c2 = Client()
print('GET /login/docente/ ->', c2.get('/login/docente/').status_code)
print('Cookie after GET /login/docente/:', c2.cookies.get('csrftoken'))
print('POST /login/docente/ ->', c2.post('/login/docente/', {'email':'nope@example.com', 'password':'x'}).status_code)
