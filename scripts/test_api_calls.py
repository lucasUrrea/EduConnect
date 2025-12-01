import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
django.setup()

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APIClient

# Ensure tokens exist for our test users
users = ['admin@example.com', 'teststudent@example.com', 'student1@example.com', 'docente1@example.com']
for u in users:
    try:
        user = User.objects.get(username=u)
        token, created = Token.objects.get_or_create(user=user)
        print(f'User {u} token: {token.key}')
    except User.DoesNotExist:
        print(f'User {u} not found in auth.User')

# Use APIClient to GET consultas (unauthenticated)
client = APIClient()
resp = client.get('/api/consultas/')
print('Unauthenticated GET /api/consultas/ status:', resp.status_code, 'count:', len(resp.data) if resp.status_code==200 else '')

# Now authenticate as student1
try:
    user = User.objects.get(username='student1@example.com')
    token = Token.objects.get(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    resp = client.get('/api/consultas/')
    print('Authenticated GET /api/consultas/ status:', resp.status_code)
    if resp.status_code == 200:
        print('First item:', resp.data[0] if resp.data else 'no items')
except Exception as e:
    print('Error during authenticated API call:', e)
