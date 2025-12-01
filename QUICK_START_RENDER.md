# 🚀 GUÍA RÁPIDA: Hosteando EduConnect en Render

**Tiempo estimado: 30 minutos**

---

## 📋 Archivos Nuevos Creados

Tu proyecto ahora tiene todos los archivos necesarios para producción:

```
✅ Procfile                    → Cómo iniciar en Render
✅ runtime.txt                 → Versión de Python
✅ requirements.txt            → Actualizado con dependencias
✅ .env.example                → Variables necesarias
✅ render.yaml                 → Configuración de servicios
✅ DEPLOYMENT_RENDER.md        → Guía completa (80+ pasos)
✅ DEPLOYMENT_SUMMARY.md       → Resumen ejecutivo
✅ generate_env_vars.py        → Generador de secrets
✅ verificar_deployment.bat    → Script de verificación
✅ .github/workflows/deploy.yml → Pipeline automático
✅ settings.py                 → Actualizado para producción
```

---

## 🎯 3 Pasos Principales

### PASO 1: Crear Repositorio GitHub (5 min)

```bash
cd "c:\Users\lucas\OneDrive\Escritorio\Modulos de consultas\Modulos de consultas"
git init
git add .
git commit -m "EduConnect ready for production"
```

Luego en https://github.com/new:
- Nombre: `educonnect`
- Público
- Copiar remoto y hacer push

### PASO 2: Configurar Render (10 min)

1. Ve a https://render.com
2. Sign up con GitHub
3. Click "New → Web Service"
4. Conecta repositorio `educonnect`
5. Configura:
   - **Build**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start**: `gunicorn modulos_consultas.wsgi`

### PASO 3: Configurar Variables (10 min)

Ejecuta localmente:
```bash
python generate_env_vars.py
```

Copia la `SECRET_KEY` que genera.

En Render → Tu servicio → Environment:
```
SECRET_KEY = [la que generaste]
DEBUG = False
ALLOWED_HOSTS = tu-app.onrender.com
DATABASE_URL = [URL de PostgreSQL en Render]
```

---

## 🎉 ¡Listo!

Tu app estará en: `https://tu-app.onrender.com`

---

## 📚 Documentación Completa

Para instrucciones más detalladas: **DEPLOYMENT_RENDER.md**

---

## ⚡ Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| Build falla | Revisa logs en Render → Logs |
| ModuleNotFoundError | Agrega a requirements.txt |
| ALLOWED_HOSTS error | Configura en Environment de Render |
| Base de datos error | Verifica DATABASE_URL |
| Archivos estáticos no cargan | Ejecuta `collectstatic` (ya en Procfile) |

---

## 📞 Soporte

- Documentación Render: https://render.com/docs
- Logs en tiempo real: Dashboard → Logs
- Status: https://status.render.com

**¡Éxito en tu deployment!** 🚀
