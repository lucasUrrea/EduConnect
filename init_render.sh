#!/bin/bash

echo "Ejecutando migraciones de Django..."
python manage.py migrate --no-input

echo "Creando superusuario de prueba..."
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin@example.com').exists():
    User.objects.create_superuser('admin@example.com', 'admin@example.com', 'admin123')
    print("Superusuario creado exitosamente")
else:
    print("Superusuario ya existe")
END

echo "Inicialización completada!"
