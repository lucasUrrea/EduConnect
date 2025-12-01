# 📋 Guía Completa: Hostear EduConnect en Render

Esta guía te mostrará cómo desplegar la aplicación Django (EduConnect) en Render, un servicio de hosting moderno y fácil de usar.

---

## 📋 Tabla de Contenidos
1. [Preparación previa](#preparación-previa)
2. [Configurar repositorio Git](#configurar-repositorio-git)
3. [Crear cuenta en Render](#crear-cuenta-en-render)
4. [Configurar base de datos](#configurar-base-de-datos)
5. [Variables de entorno](#variables-de-entorno)
6. [Desplegar la aplicación](#desplegar-la-aplicación)
7. [Verificación post-deployment](#verificación-post-deployment)
8. [Solucionar problemas](#solucionar-problemas)

---

## 🔧 Preparación previa

### Requisitos instalados:
- ✅ Git
- ✅ Cuenta GitHub
- ✅ Cuenta Render (crear en render.com)

### Archivos ya creados en el proyecto:
- ✅ `Procfile` - Define cómo iniciar la aplicación
- ✅ `runtime.txt` - Especifica versión de Python (3.13.2)
- ✅ `requirements.txt` - Actualizado con dependencias de producción
- ✅ `.env.example` - Plantilla de variables de entorno
- ✅ `render.yaml` - Configuración de servicios para Render
- ✅ `modulos_consultas/settings.py` - Actualizado para producción

---

## 🚀 Configurar repositorio Git

### Paso 1: Inicializar Git (si no está hecho)
```bash
cd "c:\Users\lucas\OneDrive\Escritorio\Modulos de consultas\Modulos de consultas"
git init
git config user.name "Tu Nombre"
git config user.email "tu.email@gmail.com"
```

### Paso 2: Crear .gitignore
Crea un archivo `.gitignore` en la raíz del proyecto:

```
.env
*.pyc
__pycache__/
*.log
db.sqlite3
staticfiles/
media/
.vscode/
.env.local
*.swp
.DS_Store
node_modules/
venv/
env/
```

### Paso 3: Agregar todos los archivos
```bash
git add .
git commit -m "Initial commit - EduConnect ready for production"
```

### Paso 4: Crear repositorio en GitHub
1. Ve a https://github.com/new
2. Crea un repositorio llamado `educonnect`
3. No inicialices con README (ya existe)
4. Copia los comandos para agregar remoto

```bash
git remote add origin https://github.com/TU_USUARIO/educonnect.git
git branch -M main
git push -u origin main
```

---

## 📱 Crear cuenta en Render

### Paso 1: Registrarse
1. Ve a https://render.com
2. Haz clic en "Sign up"
3. Conecta tu cuenta GitHub
4. Autoriza a Render

### Paso 2: Crear nuevo servicio web
1. Dashboard → New → Web Service
2. Conecta tu repositorio de GitHub
3. Configura los detalles:
   - **Name**: `educonnect` (o el nombre que prefieras)
   - **Environment**: `Python 3`
   - **Region**: Elige la más cercana a tus usuarios
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn modulos_consultas.wsgi`

---

## 💾 Configurar base de datos

### Opción A: PostgreSQL en Render (Recomendado)

1. En Render Dashboard → New → PostgreSQL
2. Configura:
   - **Name**: `educonnect-db`
   - **Database**: `educonnect_db`
   - **User**: `educonnect_user`
   - **Region**: Misma que el servicio web
   - **Plan**: Free (para desarrollo/pruebas)

3. Copia la `Internal Database URL`

### Opción B: MySQL externo

Si prefieres mantener tu MySQL actual:
1. Asegúrate de que sea accesible desde internet
2. Usa la URL: `mysql://user:password@host:3306/database`

---

## 🔐 Variables de entorno

En Render, necesitas configurar variables de entorno. Ve a tu servicio web en Render y haz clic en "Environment":

### Variables requeridas:

```
SECRET_KEY = [Genera una nueva clave secreta segura]
DEBUG = False
ALLOWED_HOSTS = tu-dominio.render.com,www.tu-dominio.com

# Para PostgreSQL
DATABASE_URL = [Copia del servicio PostgreSQL]

# Para MySQL externo
DB_ENGINE = django.db.backends.mysql
DB_NAME = tu_base_datos
DB_USER = tu_usuario
DB_PASSWORD = tu_contraseña
DB_HOST = tu_host
DB_PORT = 3306

# Seguridad
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Email (para password resets)
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = tu-email@gmail.com
EMAIL_HOST_PASSWORD = [Clave de aplicación de Gmail]
```

### ⚠️ Generar SECRET_KEY segura

En tu computadora:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y pégalo en `SECRET_KEY` en Render.

---

## 🚀 Desplegar la aplicación

### Primera vez: Deploy Manual
1. En Render Dashboard, selecciona tu servicio web
2. Haz clic en "Manual Deploy"
3. Espera a que se complete (3-5 minutos)

### Deploys automáticos (recomendado)
1. En tu servicio web en Render
2. Conecta a tu rama `main` de GitHub
3. Cada `git push` a `main` iniciará un deployment automático

### Monitorear el deploy
1. Ve a "Logs" en Render
2. Verás el progreso en tiempo real
3. Espera el mensaje "Your service is live"

---

## ✅ Verificación post-deployment

### Paso 1: Acceder a la aplicación
- Tu dominio será: `https://educonnect.onrender.com` (o similar)
- Si compraste un dominio personalizado, úsalo en Render Settings

### Paso 2: Verificar funcionalidades
1. ✅ Ir a la página de login
2. ✅ Iniciar sesión con credenciales de prueba
3. ✅ Crear una consulta como estudiante
4. ✅ Ver consulta como profesor
5. ✅ Responder y editar respuesta

### Paso 3: Ver logs
En Render → Logs, verifica que no haya errores

### Paso 4: Crear usuario admin
Si necesitas acceso admin:
```bash
# Conectarse a través de Render Shell (si está disponible)
python manage.py createsuperuser
```

---

## 🐛 Solucionar problemas

### Error: "ModuleNotFoundError: No module named 'decouple'"
**Solución**: Asegúrate de que `python-decouple==3.8` está en `requirements.txt`

### Error: "ALLOWED_HOSTS"
**Solución**: En Render Variables de entorno, agrega tu dominio a `ALLOWED_HOSTS`

### Error: "ProgrammingError" con base de datos
**Solución**: 
1. Ve a "Logs" en Render
2. Mira el error específico
3. Ejecuta migraciones: incluye en Build Command si no está

### Error: "403 Forbidden"
**Solución**: Verifica `CSRF_TRUSTED_ORIGINS` en settings.py o agrega dominio

### La aplicación inicia pero es lenta
**Solución**: Aumenta el plan a "Starter" en Render (no es free pero es muy económico)

---

## 📊 Monitorear en producción

### Logs
- Ve a Render Dashboard → Tu servicio → Logs
- Filtra por tipo de mensaje

### Métricas
- CPU, RAM, red en tiempo real
- Alertas automáticas si algo falla

### Variables de entorno
- Úpdalas sin hacer redeploy
- Render reinicia automáticamente

---

## 💡 Mejores prácticas para producción

1. **Secretos seguros**: Nunca commitees `.env` con valores reales
2. **Backups**: Configura backups automáticos en la BD
3. **Emails**: Usar SendGrid, Mailgun o servicio de email profesional
4. **CDN**: Considera Cloudflare para acelerar contenido estático
5. **Monitoreo**: Configura alertas en Render
6. **Domain**: Compra un dominio en Namecheap y configúralo en Render
7. **SSL**: Automático en Render (certificado Let's Encrypt)

---

## 📝 Checklist final

Antes de ir a producción:

- [ ] Git repository creado y sincronizado
- [ ] `.gitignore` configurado
- [ ] Todas las dependencias en `requirements.txt`
- [ ] `DEBUG = False` en producción
- [ ] `SECRET_KEY` segura configurada
- [ ] Base de datos migrada
- [ ] Static files recolectados
- [ ] Email configurado (opcional pero recomendado)
- [ ] Dominio custom configurado (opcional)
- [ ] SSL/HTTPS activo
- [ ] Pruebas finales realizadas

---

## 🎉 ¡Felicidades!

Tu aplicación EduConnect está lista para producción en Render. 

**Próximos pasos**:
1. Monitorea los logs regularmente
2. Crea usuarios de prueba en producción
3. Comunica a tus usuarios el nuevo dominio
4. Mantén backups regularmente

---

**Dudas o problemas?** Revisa la documentación oficial de Render: https://render.com/docs
