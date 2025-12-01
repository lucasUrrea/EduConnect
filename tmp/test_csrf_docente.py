import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
sys.path.insert(0, os.getcwd())
import django
django.setup()

from django.test import Client
from EduConnectApp.models import Usuarios

c = Client()
# GET the docente login page to set cookies and CSRF token
r = c.get('/login/docente/')
print('GET status', r.status_code)
# Read token from form hidden input if present
from bs4 import BeautifulSoup
soup = BeautifulSoup(r.content, 'html.parser')
input_token = soup.find('input', {'name':'csrfmiddlewaretoken'})
print('Form token present:', bool(input_token))
cookie_token = c.cookies.get('csrftoken')
print('Cookie token present:', cookie_token.value if cookie_token else None)

# Attempt to POST with wrong token first (should be rejected)
resp_wrong = c.post('/login/docente/', {'email':'nope@example.com', 'password':'x'})
print('POST wrong token status', resp_wrong.status_code)
# Now ensure correct token is used by client (Client handles it automatically if cookie present)
resp = c.post('/login/docente/', {'email':'nope@example.com', 'password':'x'})
print('POST status (with client-managed token):', resp.status_code)
