import os, sys, re, json
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
import django
django.setup()
from EduConnectApp.models import Usuarios, Estudiantes, Asignaturas, Consultas
from django.contrib.auth.models import User
from django.utils import timezone

# create test user + estudiante + django user
email = 'webtest@example.com'
password = 'testpass'
print('Ensuring test user exists...')
usuario, created = Usuarios.objects.get_or_create(email=email, defaults={
    'password_hash': 'pbkdf2_sha256$1000000$test$hash',
    'tipo_usuario': 'estudiante',
    'nombre': 'Web',
    'apellido_paterno': 'Tester',
    'estado': 'activo'
})
if created:
    print('Created Usuarios record')
else:
    print('Usuarios exists')

# ensure Django user with same password
du, duc = User.objects.get_or_create(username=email, defaults={'email': email, 'first_name':'Web','last_name':'Tester'})
if duc:
    du.set_password(password)
    du.save()
    print('Created Django user with password')
else:
    # ensure password set
    du.set_password(password)
    du.save()
    print('Ensured Django user and password updated')

# ensure Estudiantes exists
est, estc = Estudiantes.objects.get_or_create(id_usuario=usuario, defaults={'numero_matricula':'WEB001'})
print('Estudiante created?', estc, 'pk=', est.pk)

# pick an asignatura
asig = Asignaturas.objects.first()
print('Using asignatura pk=', asig.pk)

# Now simulate HTTP login and POST using urllib (cookie handling)
import http.cookiejar, urllib.request, urllib.parse
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

base = 'http://127.0.0.1:8000'

# Get login page to obtain CSRF cookie
print('Fetching login page...')
resp = opener.open(base + '/login/')
html = resp.read().decode('utf-8')
# try to find csrfmiddlewaretoken in HTML
m = re.search(r"name=['\"]csrfmiddlewaretoken['\"] value=['\"]([0-9a-zA-Z]+)['\"]", html)
if m:
    token = m.group(1)
else:
    # fall back to cookie
    token = None
for cookie in cj:
    if cookie.name == 'csrftoken':
        csrf_cookie = cookie.value
        break
    else:
        csrf_cookie = None
print('csrf token from form:', token, 'csrf cookie:', csrf_cookie)

# Post login credentials
login_data = urllib.parse.urlencode({'email': email, 'password': password, 'csrfmiddlewaretoken': csrf_cookie}).encode('utf-8')
req = urllib.request.Request(base + '/login/', data=login_data, method='POST')
req.add_header('Referer', base + '/login/')
resp = opener.open(req)
print('Login response URL:', resp.geturl())

# Now GET crear_consulta to grab CSRF token (correct URL path)
resp = opener.open(base + '/consulta/crear/')
html = resp.read().decode('utf-8')
# find token
m = re.search(r"name=['\"]csrfmiddlewaretoken['\"] value=['\"]([0-9a-zA-Z]+)['\"]", html)
if m:
    token = m.group(1)
else:
    token = None
for cookie in cj:
    if cookie.name == 'csrftoken':
        csrf_cookie = cookie.value
print('Crear csrf token:', token, 'cookie:', csrf_cookie)

# Post a new consulta
post_data = {
    'id_asignatura': str(asig.id_asignatura),
    'id_categoria': '',
    'titulo': 'Consulta web test via script',
    'descripcion': 'Esta consulta fue creada por script web test',
    'prioridad': '',
    'csrfmiddlewaretoken': csrf_cookie
}
post = urllib.parse.urlencode(post_data).encode('utf-8')
req = urllib.request.Request(base + '/consulta/crear/', data=post, method='POST')
req.add_header('Referer', base + '/consulta/crear/')
resp = opener.open(req)
print('After POST, redirected to:', resp.geturl())

# Check DB for the created titulo
found = Consultas.objects.filter(titulo='Consulta web test via script').order_by('-fecha_consulta')
print('Found in DB count:', found.count())
if found.exists():
    c = found.first()
    print('Consulta:', c.pk, c.titulo, c.id_estudiante.id_estudiante, c.id_estudiante.id_usuario_id, c.fecha_consulta)
else:
    print('Not found')
