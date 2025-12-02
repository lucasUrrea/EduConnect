from django.contrib.auth.models import User
from EduConnectApp.models import Usuarios
from django.utils import timezone

print("\n=== Creating Admin User ===")
try:
    if not User.objects.filter(username='admin@example.com').exists():
        User.objects.create_superuser('admin@example.com', 'admin@example.com', 'admin123')
        print("✅ Admin created: admin@example.com / admin123")
    else:
        print("✅ Admin already exists")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n=== Creating Student User ===")
try:
    if not Usuarios.objects.filter(email='student1@example.com').exists():
        user = User.objects.create_user('student1@example.com', 'student1@example.com', 'studpass')
        Usuarios.objects.create(
            email='student1@example.com',
            nombre='Joseph',
            apellido_paterno='Nohra',
            apellido_materno='',
            tipo_usuario='estudiante',
            estado='activo',
            password_hash=user.password,
            telefono='',
            direccion='',
            fecha_creacion=timezone.now(),
            fecha_actualizacion=timezone.now()
        )
        print("✅ Student created: student1@example.com / studpass")
    else:
        print("✅ Student already exists")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n=== Creating Teacher User ===")
try:
    if not Usuarios.objects.filter(email='docente1@example.com').exists():
        user = User.objects.create_user('docente1@example.com', 'docente1@example.com', 'docpass')
        Usuarios.objects.create(
            email='docente1@example.com',
            nombre='Sebastian',
            apellido_paterno='Pizarro',
            apellido_materno='',
            tipo_usuario='docente',
            estado='activo',
            password_hash=user.password,
            telefono='',
            direccion='',
            fecha_creacion=timezone.now(),
            fecha_actualizacion=timezone.now()
        )
        print("✅ Teacher created: docente1@example.com / docpass")
    else:
        print("✅ Teacher already exists")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n✅ Database initialization complete!")
