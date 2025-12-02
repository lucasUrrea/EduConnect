release: python manage.py migrate --no-input && python manage.py shell < initialize_db.py
web: gunicorn modulos_consultas.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
