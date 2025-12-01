# 🎬 Tutorial Paso a Paso: Hostear en Render (Versión Escrita)

## 📹 Duración: 30 minutos
## 👥 Para: Cualquiera que quiera hosteear EduConnect en producción

---

## 🎯 Lo que lograrás

Al final de este tutorial:
- ✅ Tu aplicación estará en vivo en internet
- ✅ Accesible desde cualquier lugar
- ✅ Con dominio de Render (gratis)
- ✅ Totalmente seguro (HTTPS)
- ✅ Con base de datos PostgreSQL

---

## 🕐 MINUTO 1-5: Preparación en GitHub

### Paso 1: Abre PowerShell

```bash
# Navega al directorio del proyecto
cd "c:\Users\lucas\OneDrive\Escritorio\Modulos de consultas\Modulos de consultas"

# Verifica que estés en el lugar correcto
ls manage.py
# Debe mostrar: manage.py
```

### Paso 2: Inicializa Git

```bash
git init
git config user.name "Tu Nombre Aquí"
git config user.email "tu.email@gmail.com"
```

### Paso 3: Agrega archivos a Git

```bash
git add .
git commit -m "EduConnect - Ready for production on Render"
```

**Resultado esperado:**
```
[main (root-commit) abc1234] EduConnect - Ready for production
 15 files changed, 1000+ insertions(+)
```

### Paso 4: Crea repositorio en GitHub

1. Ve a https://github.com/new
2. **Repository name**: `educonnect`
3. **Description**: EduConnect - Sistema de consultas académicas
4. ☑️ **Public**
5. Click **Create repository**

### Paso 5: Conecta con GitHub

En PowerShell, copia estos comandos (cambia `TU_USUARIO`):

```bash
git remote add origin https://github.com/TU_USUARIO/educonnect.git
git branch -M main
git push -u origin main
```

Ingresa tu usuario/token de GitHub cuando se pida.

**Resultado esperado:**
```
Enumerating objects: 15, done.
...
 * [new branch]      main -> main
```

---

## 🕐 MINUTO 6-10: Preparar Variables de Entorno

### Paso 6: Generar SECRET_KEY segura

En PowerShell, desde el directorio del proyecto:

```bash
python generate_env_vars.py
```

**Resultado esperado:**
```
================================================================================
  GENERADOR DE VARIABLES DE ENTORNO SEGURAS
================================================================================

🔐 SECRET_KEY (cópiala a tu .env en Render):
   django-insecure-abc123def456ghi789jkl...
```

**👉 Copia esta clave, la necesitaremos en un minuto**

---

## 🕐 MINUTO 11-16: Configurar Render

### Paso 7: Crear cuenta en Render

1. Ve a https://render.com
2. Click **Sign up**
3. Click **Continue with GitHub**
4. Autoriza a Render
5. Click **Authorize render**

### Paso 8: Crear nuevo Web Service

En Render Dashboard:
1. Click azul **+ New**
2. Selecciona **Web Service**
3. Haz clic en conectar repositorio
4. Selecciona **educonnect**
5. Click **Connect**

### Paso 9: Configurar el Web Service

Rellena los campos:

| Campo | Valor |
|-------|-------|
| **Name** | `educonnect` |
| **Environment** | `Python 3` |
| **Region** | Elige el más cercano a tu ubicación |
| **Build Command** | `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput` |
| **Start Command** | `gunicorn modulos_consultas.wsgi` |
| **Instance Type** | Free |

**👉 NO hagas click en Deploy aún**

### Paso 10: Agregar variables de entorno

Antes de desplegar, agrega las variables:

1. Scroll hacia abajo a **Environment**
2. Click **Add Environment Variable**
3. Para cada variable, rellena:

```
SECRET_KEY = [Aquella que copiaste en Paso 6]
```

4. Click **+** y agrega:

```
DEBUG = False
```

5. Click **+** y agrega:

```
ALLOWED_HOSTS = *.onrender.com
```

Debe verse así:
```
SECRET_KEY = django-insecure-abc123...
DEBUG = False
ALLOWED_HOSTS = *.onrender.com
```

---

## 🕐 MINUTO 17-20: Crear Base de Datos

### Paso 11: Crear PostgreSQL en Render

En Render Dashboard:
1. Click azul **+ New**
2. Selecciona **PostgreSQL**
3. Rellena:

| Campo | Valor |
|-------|-------|
| **Name** | `educonnect-db` |
| **Database** | `educonnect_db` |
| **User** | `educonnect` |
| **Region** | Misma que el Web Service |
| **Plan** | Free |

4. Click **Create Database**

### Paso 12: Obtener DATABASE_URL

La BD se está creando. Una vez lista:
1. Click en el nombre de la BD
2. Scroll a **Connections**
3. Copia la **Internal Database URL** (algo como: `postgresql://...`)

**👉 Cópiala, la necesitamos**

### Paso 13: Agregar DATABASE_URL al Web Service

1. Vuelve a tu Web Service (click en "educonnect" en Dashboard)
2. Click **Environment**
3. Click **Add Environment Variable**
4. Pega la URL:

```
DATABASE_URL = postgresql://euconnect:pqxx...@localhost:5432/educonnect_db
```

---

## 🕐 MINUTO 21-25: Deploy

### Paso 14: Iniciar deployment

En tu Web Service ("educonnect"):
1. Scroll al final
2. Click azul **Create Web Service**

**Verás que está en "Build in progress"**

### Paso 15: Espera a que termine

Ve a **Logs** (pestaña en el mismo Web Service)

Verás algo como:
```
Started building your service
Installing dependencies...
...
Successfully deployed
Your service is live on https://educonnect.onrender.com
```

**Esto toma 3-5 minutos**

Puedes ir a tomar café ☕ mientras esperas.

---

## 🕐 MINUTO 26-30: Verificación Final

### Paso 16: Accede a tu aplicación

1. Una vez que Render diga "Your service is live"
2. Click en el link: `https://educonnect.onrender.com`
3. ¡Tu aplicación está en internet! 🎉

### Paso 17: Pruebas finales

1. **Ir a login**
2. **Iniciar sesión** (usa credenciales que tenías localmente)
3. **Crear una consulta** como estudiante
4. **Cambiar de usuario** a profesor
5. **Ver la consulta** en el dashboard

**Si todo funciona: ¡Éxito! 🎉**

### Paso 18: Agregar dominio personalizado (opcional)

Si compraste un dominio en Namecheap:

1. En Render → Tu Web Service → **Custom Domain**
2. Ingresa: `www.midominio.com`
3. Sigue instrucciones para actualizar DNS en Namecheap

---

## 🐛 Solución Rápida de Problemas

### Error: "Build failed"
- Ve a **Logs** → busca el error rojo
- Verifica requirements.txt tenga todas las librerías
- Asegúrate de que todos los archivos se subieron a GitHub

### Error: "Application failed to start"
- Revisa **Logs** → busca el error
- Verifica que ALLOWED_HOSTS contenga tu dominio
- Comprueba que DATABASE_URL esté configurada

### Error: "Database connection refused"
- Espera 2 minutos a que PostgreSQL esté lista
- Verifica DATABASE_URL no tenga espacios
- Prueba copiar-pegar nuevamente

### Error: "Página en blanco"
- F12 (Abre Developer Tools)
- Tab **Console** para ver errores
- Verifica logs en Render Dashboard

---

## ✅ Checklist de Verificación

Marca cada paso completado:

- [ ] Git inicializado
- [ ] Código subido a GitHub
- [ ] Cuenta Render creada
- [ ] Web Service configurado
- [ ] Variables de entorno agregadas
- [ ] PostgreSQL creada
- [ ] DATABASE_URL configurada
- [ ] Deploy completado
- [ ] App accesible en https://educonnect.onrender.com
- [ ] Login funciona
- [ ] Consultas se crean
- [ ] Profesor ve consultas

---

## 🎉 ¡Congratulations!

Tu aplicación **EduConnect** está en vivo en internet.

### Próximos pasos:
1. **Comparte el link** con otros usuarios
2. **Monitorea los logs** en Render
3. **Haz cambios locales** y haz `git push` para actualizar
4. **Si crece mucho**: Upgrade a plan Starter ($7/mes)

---

## 📱 Ahora tu app es accesible desde:
- 💻 Tu computadora
- 📱 Tu teléfono
- 🌍 Cualquier lugar en el mundo
- 🔒 Completamente seguro con HTTPS

---

## 🚀 ¿Qué aprendiste?

1. Versionamiento con Git
2. Deployment en la nube
3. Configuración de variables de entorno
4. Bases de datos en la nube
5. Deployment automático desde GitHub

**Todo esto en 30 minutos.** 

Muy bien hecho. 👏

---

## 📞 ¿Necesitas ayuda?

- Render Docs: https://render.com/docs
- Revisa **FAQ_RENDER.md** en tu proyecto
- Verifica logs en Render Dashboard

---

**Última actualización:** 1 de Diciembre, 2025
**Dificultad:** Principiante/Intermedio
**Tiempo total:** 30 minutos
**Resultado:** ✅ Aplicación en vivo
