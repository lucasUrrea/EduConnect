web: gunicorn modulos_consultas.wsgi:application --log-file - --timeout 120
release: python manage.py migrate --no-input || true
