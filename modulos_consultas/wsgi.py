"""
WSGI config for modulos_consultas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')

# Obtener la aplicación Django
application = get_wsgi_application()

# Ejecutar inicialización si estamos en Render (DATABASE_URL present)
if os.environ.get('DATABASE_URL'):
    try:
        # Ejecutar inicialización una sola vez
        if not os.environ.get('DJANGO_INITIALIZED'):
            print("\n" + "="*60)
            print("INITIALIZING DJANGO APPLICATION (RENDER)")
            print("="*60)
            
            # Importar después de get_wsgi_application()
            from initialize_db import initialize_database
            initialize_database()
            
            # Marcar como inicializado
            os.environ['DJANGO_INITIALIZED'] = '1'
            
            print("="*60)
            print("INITIALIZATION COMPLETE - APP READY")
            print("="*60 + "\n")
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()

