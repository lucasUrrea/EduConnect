import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
django.setup()

from django.contrib.auth.models import User

email = 'docente1@example.com'
password = 'DocPass123!'

u = User.objects.filter(username=email).first()
if u:
    u.set_password(password)
    u.save()
    print(f"Password set for {email}")
else:
    print(f"User {email} not found; nothing changed")
