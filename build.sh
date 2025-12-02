#!/bin/bash

echo "=== INSTALANDO DEPENDENCIAS ==="
pip install -r requirements.txt

echo "=== RECOPILANDO ARCHIVOS ESTÁTICOS ==="
python manage.py collectstatic --no-input --clear

echo "=== INTENTANDO MIGRACIONES (puede fallar en build) ==="
python manage.py migrate --no-input || echo "Migraciones no disponibles durante build (esperado)"

echo "=== BUILD COMPLETADO ==="