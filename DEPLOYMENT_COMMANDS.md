#!/bin/bash
# 📋 DEPLOYMENT COMMANDS - Todos los comandos necesarios
# Este archivo contiene todos los comandos para desplegar en Render
# Copia y pega según necesites

# ============================================================================
# FASE 1: PREPARACIÓN LOCAL
# ============================================================================

# Navega al directorio del proyecto
cd "c:\Users\lucas\OneDrive\Escritorio\Modulos de consultas\Modulos de consultas"

# Inicializa Git
git init
git config user.name "Tu Nombre"
git config user.email "tu.email@gmail.com"

# Crea .gitignore (si no existe)
# Ver DEPLOYMENT_RENDER.md para contenido

# Agrega todos los archivos
git add .

# Commit inicial
git commit -m "Initial commit - EduConnect ready for production"

# ============================================================================
# FASE 2: CONFIGURACIÓN GITHUB
# ============================================================================

# Ve a https://github.com/new y crea repositorio "educonnect"

# Después de crear el repositorio, ejecuta:
git remote add origin https://github.com/TU_USUARIO/educonnect.git
git branch -M main
git push -u origin main

# Para actualizaciones posteriores:
git add .
git commit -m "Descripción del cambio"
git push origin main

# ============================================================================
# FASE 3: GENERAR VARIABLES DE ENTORNO
# ============================================================================

# Genera SECRET_KEY segura
python generate_env_vars.py

# Salida esperada: Una clave larga y segura
# Cópiala para usarla en Render

# ============================================================================
# FASE 4: CREAR CUENTA RENDER
# ============================================================================

# Ve a https://render.com
# Click "Sign up" → Conecta GitHub → Autoriza

# ============================================================================
# FASE 5: CREAR WEB SERVICE EN RENDER
# ============================================================================

# En Render Dashboard:
# 1. Click "New" → "Web Service"
# 2. Conecta repositorio "educonnect"
# 3. Configura detalles:

# Name: educonnect (o tu nombre)
# Environment: Python 3
# Region: [Elige el más cercano]
# Build Command: 
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput

# Start Command:
gunicorn modulos_consultas.wsgi

# ============================================================================
# FASE 6: CONFIGURAR VARIABLES DE ENTORNO EN RENDER
# ============================================================================

# En Render Dashboard → Tu Web Service → Environment
# Agrega estas variables:

# === REQUERIDAS ===
SECRET_KEY=<resultado de generate_env_vars.py>
DEBUG=False
ALLOWED_HOSTS=tu-app.onrender.com

# === BASE DE DATOS ===
# Opción A: PostgreSQL en Render
DATABASE_URL=<URL que proporcionó PostgreSQL>

# Opción B: MySQL externo
DB_ENGINE=django.db.backends.mysql
DB_NAME=tu_database
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=tu_host
DB_PORT=3306

# === SEGURIDAD ===
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# ============================================================================
# FASE 7: CREAR BASE DE DATOS (Opcional - Si no tienes externa)
# ============================================================================

# En Render Dashboard:
# 1. Click "New" → "PostgreSQL"
# 2. Configura:
#    - Name: educonnect-db
#    - Database: educonnect_db
#    - User: educonnect_user
#    - Region: [Misma que Web Service]
#    - Plan: Free (para empezar)
# 3. Copia "Internal Database URL"
# 4. Agrégala como DATABASE_URL en Web Service

# ============================================================================
# FASE 8: DEPLOY
# ============================================================================

# En Render Dashboard:
# 1. Ve a tu Web Service
# 2. Click "Manual Deploy"
# 3. Espera a que diga "Your service is live"
# 4. Click en el link de tu dominio

# ============================================================================
# FASE 9: VERIFICACIÓN
# ============================================================================

# Verifica que tu app funciona:
# 1. Ve a https://tu-app.onrender.com
# 2. Intenta iniciar sesión
# 3. Crea una consulta como estudiante
# 4. Verifica que aparezca en profesor

# Verifica logs:
# En Render Dashboard → Logs
# Debe mostrar:
# "Successfully started service" o similar

# ============================================================================
# FASE 10: ACTUALIZACIONES FUTURAS
# ============================================================================

# Para hacer cambios:

# 1. Modifica el código localmente
git add .
git commit -m "Descripción del cambio"
git push origin main

# 2. Render redeploya automáticamente
# 3. Los logs aparecen en Render Dashboard → Logs

# ============================================================================
# COMANDOS ÚTILES PARA MAINTENANCE
# ============================================================================

# Ver logs en tiempo real:
# Render Dashboard → Tu Web Service → Logs

# Resetear base de datos (CUIDADO - Borra datos):
# Render Dashboard → Tu PostgreSQL → Data → Delete Data

# Ejecutar comando en Render:
# Render Dashboard → Shell → Escribe comando

# Escalar a plan Starter (más recursos):
# Render Dashboard → Settings → Plan

# Conectar dominio personalizado:
# Render Dashboard → Settings → Custom Domain

# ============================================================================
# TROUBLESHOOTING RÁPIDO
# ============================================================================

# Si falla el build:
# - Revisa logs en Render Dashboard
# - Verifica requirements.txt
# - Comprueba que todos los archivos estén en GitHub

# Si falla al iniciar:
# - Ve a Render Dashboard → Logs
# - Busca el error específico
# - Compara con FAQ_RENDER.md

# Si la BD no conecta:
# - Verifica DATABASE_URL en Environment
# - Comprueba que PostgreSQL esté en Render
# - Revisa credenciales

# Si archivos estáticos no cargan:
# - Verificar que WhiteNoise esté en requirements.txt
# - Comprobar que collectstatic esté en Build Command
# - Revisar STATIC_URL y STATIC_ROOT en settings.py

# Si emails no funcionan:
# - Configurar EMAIL_HOST_PASSWORD con App Password (Gmail)
# - O usar SendGrid en lugar de Gmail

# ============================================================================
# COMANDOS LOCALES ÚTILES (para desarrollo)
# ============================================================================

# Recolectar archivos estáticos localmente:
python manage.py collectstatic

# Ejecutar migraciones locales:
python manage.py migrate

# Crear usuario admin:
python manage.py createsuperuser

# Ver estado de la BD:
python manage.py dbshell

# Resetear BD (SOLO desarrollo):
rm db.sqlite3
python manage.py migrate

# Verificar deployment readiness:
./verificar_deployment.bat  (Windows)
bash verificar_deployment.sh (Linux/Mac)

# ============================================================================
# NOTAS IMPORTANTES
# ============================================================================

# 1. NUNCA comitees .env con valores reales
# 2. SIEMPRE usa .env.example como plantilla
# 3. En producción: DEBUG SIEMPRE False
# 4. SECRET_KEY debe ser única y segura
# 5. ALLOWED_HOSTS debe tener tu dominio
# 6. DATABASE_URL nunca debe estar en código
# 7. Backup de BD regularmente en Render

# ============================================================================
# REFERENCIA RÁPIDA: URLs
# ============================================================================

# Render Dashboard: https://render.com/dashboard
# Documentación Render: https://render.com/docs
# GitHub: https://github.com
# Django Docs: https://docs.djangoproject.com
# Gunicorn: https://gunicorn.org/
# WhiteNoise: http://whitenoise.evans.io/

# ============================================================================
# ¡LISTO!
# ============================================================================

# Tu aplicación estará en: https://tu-app.onrender.com
# Logs: Render Dashboard → Logs
# Actualizaciones: git push origin main

echo "✅ ¡Deployment completado!"
echo "🌐 Tu app está en: https://tu-app.onrender.com"
echo "📊 Logs en: Render Dashboard → Logs"
echo "📝 Para cambios: git push origin main"
