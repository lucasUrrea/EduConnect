#!/bin/bash

echo "=== INSTALANDO DEPENDENCIAS ==="
pip install -r requirements.txt

echo "=== RECOPILANDO ARCHIVOS ESTÁTICOS ==="
python manage.py collectstatic --no-input --clear || echo "Aviso: collectstatic no pudo completarse (esperado durante build)"

echo "=== BUILD COMPLETADO ==="
echo "Las migraciones y usuarios se crearán automáticamente al iniciar la app"