#!/usr/bin/env python
"""
Script para generar y configurar valores seguros para variables de entorno
Uso: python generate_env_vars.py
"""

from django.core.management.utils import get_random_secret_key
import secrets
import string


def generate_secret_key():
    """Genera una SECRET_KEY segura para Django"""
    return get_random_secret_key()


def generate_secure_password(length=32):
    """Genera una contraseña segura"""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


def main():
    print("\n" + "="*70)
    print("  GENERADOR DE VARIABLES DE ENTORNO SEGURAS")
    print("="*70 + "\n")
    
    # Generar SECRET_KEY
    secret_key = generate_secret_key()
    print("🔐 SECRET_KEY (cópiala a tu .env en Render):")
    print(f"   {secret_key}\n")
    
    # Generar contraseña segura
    db_password = generate_secure_password()
    print("🔒 DATABASE_PASSWORD segura:")
    print(f"   {db_password}\n")
    
    # Mostrar resumen
    print("="*70)
    print("  INSTRUCCIONES PARA RENDER")
    print("="*70)
    print("""
1. En Render Dashboard, ve a tu Web Service
2. Haz clic en "Environment" 
3. Agrega estas variables:

   SECRET_KEY = <la clave generada arriba>
   DEBUG = False
   ALLOWED_HOSTS = tu-dominio.render.com,www.tu-dominio.com
   
4. Si usas PostgreSQL externo, agrega también:
   
   DATABASE_URL = postgresql://user:password@host:port/dbname

5. Guarda los cambios

Nota: Las variables de entorno se aplican al reiniciar el servicio.
    """)
    
    print("="*70 + "\n")


if __name__ == '__main__':
    import os
    import django
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
    django.setup()
    
    main()
