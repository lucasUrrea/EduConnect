import os, sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
import django
django.setup()
from django.test import Client
from EduConnectApp.models import Usuarios, Estudiantes, Asignaturas, Consultas

c = Client()
email='webtest@example.com'
password='testpass'
# login via POST
resp = c.post('/login/', {'email': email, 'password': password})
print('login status', resp.status_code, 'redirected to', resp['Location'] if 'Location' in resp else None)
# check session values
sess = c.session
print('session keys after login:', list(sess.keys()))
# create consulta
asig = Asignaturas.objects.first()
resp2 = c.post('/consulta/crear/', {'id_asignatura': asig.id_asignatura, 'titulo':'Client created consulta', 'descripcion':'Created by test client'}, follow=True)
print('post crear status', resp2.status_code)
# see if created
found = Consultas.objects.filter(titulo='Client created consulta')
print('Found count:', found.count())
if found.exists():
    cobj = found.order_by('-fecha_consulta').first()
    print('Created consulta pk=', cobj.pk, 'estudiante_id=', cobj.id_estudiante.id_estudiante)
else:
    print('No created consulta found')
