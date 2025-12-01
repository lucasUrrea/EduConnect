import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
django.setup()

from django.contrib.auth.models import User
from EduConnectApp.models import Usuarios, Estudiantes

created = []

# Superuser for admin
admin_username = 'admin@example.com'
admin_password = 'AdminPass123!'
if not User.objects.filter(username=admin_username).exists():
    User.objects.create_superuser(admin_username, admin_username, admin_password)
    created.append(('admin', admin_username, admin_password))

# Test student user
student_email = 'teststudent@example.com'
student_password = 'TestPass123!'
if not Usuarios.objects.filter(email=student_email).exists():
    u = Usuarios.objects.create(
        email=student_email,
        password_hash=make_password(student_password),
        tipo_usuario='estudiante',
        nombre='Test',
        apellido_paterno='Student',
        estado='activo'
    )
    # ensure corresponding django User
    django_user, _ = User.objects.get_or_create(username=student_email, defaults={'email': student_email, 'first_name': 'Test', 'last_name': 'Student'})
    django_user.set_password(student_password)
    django_user.save()
    Estudiantes.objects.create(id_usuario=u, numero_matricula='MAT0001')
    created.append(('student', student_email, student_password))

if created:
    print('Created users:')
    for role, user, pwd in created:
        print(f'- {role}: {user} / {pwd}')
else:
    print('No new users created (already exist).')
