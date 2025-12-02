#!/bin/bash

pip install -r requirements.txt

# Only run migrations if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "DATABASE_URL not set, skipping migrations during build"
else
    python manage.py migrate --no-input
fi

python manage.py collectstatic --no-input
