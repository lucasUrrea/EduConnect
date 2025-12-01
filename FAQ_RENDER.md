# ❓ Preguntas Frecuentes - Deployment en Render

## 1. ¿Cuánto cuesta hostear en Render?

**R:** 
- **Free tier**: Perfecto para desarrollo/pruebas
- **Starter** ($7/mes): Mejor para aplicaciones reales
- **Pro** ($12+/mes): Mayor performance

La BD PostgreSQL free se reinicia si no hay actividad en 15 min.

---

## 2. ¿Puedo usar mi base de datos MySQL actual en lugar de PostgreSQL?

**R:** Sí. Necesitas:
1. Asegurar que tu MySQL sea accesible desde internet
2. En Render → Environment:
   ```
   DB_ENGINE = django.db.backends.mysql
   DB_NAME = tu_base_datos
   DB_USER = usuario
   DB_PASSWORD = contraseña
   DB_HOST = tuhost.com
   DB_PORT = 3306
   ```

---

## 3. ¿Qué pasa con mis archivos subidos (media)?

**R:** Con Render free:
- Los archivos se pierden si reinicia la BD (15 min sin uso)
- **Solución**: Usar almacenamiento externo:
  - AWS S3
  - Google Cloud Storage
  - Cloudinary

Para desarrollo, está bien usar media local.

---

## 4. ¿Cómo actualizo la aplicación sin perder datos?

**R:**
1. Haz cambios localmente
2. Commit y push a GitHub:
   ```bash
   git add .
   git commit -m "Descripción del cambio"
   git push origin main
   ```
3. Render redeploya automáticamente
4. Las migraciones se ejecutan automáticamente

---

## 5. ¿Mi dominio actual funcionará?

**R:** Sí:
1. Compra/usa dominio en Namecheap o similar
2. En Render → Settings → Custom Domain
3. Sigue instrucciones para configurar DNS

---

## 6. ¿Cómo hago que los emails funcionen?

**R:** Necesitas un servicio de email:

**Opción 1: Gmail (gratis, limitado)**
```
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = tu-email@gmail.com
EMAIL_HOST_PASSWORD = [Contraseña de app - ver nota]
```

**Opción 2: SendGrid (profesional)**
- Cuenta free en sendgrid.com
- Más confiable para producción

---

## 7. ¿Por qué dice "Waiting for build"?

**R:** Render está:
1. Descargando tu código
2. Instalando dependencias
3. Ejecutando migraciones
4. Recolectando archivos estáticos

Esto toma 3-5 minutos la primera vez.

---

## 8. ¿Cómo veo los errores en producción?

**R:** 
1. En Render Dashboard
2. Click en tu servicio
3. Tab "Logs"
4. Ver logs en tiempo real

---

## 9. ¿Qué pasa si el servidor se cae?

**R:** Render:
- Reinicia automáticamente
- Notifica por email
- Logs disponibles en Dashboard

---

## 10. ¿Necesito configurar HTTPS?

**R:** NO, es automático:
- Render proporciona certificados SSL/TLS
- Tu sitio es `https://tuapp.onrender.com`
- Dominio personalizado también tiene HTTPS

---

## 11. ¿Cuántos usuarios puede soportar?

**R:** Depende del plan:
- **Free**: Bueno para pruebas, ~100 usuarios
- **Starter**: 1,000+ usuarios concurrentes
- **Pro**: Escalable a millones

---

## 12. ¿Cómo hago backups de la base de datos?

**R:**
- Render hace backups automáticos cada 24 horas
- Opción manual: PostgreSQL Tools o adminer
- Para mayor seguridad: usar AWS RDS

---

## 13. El servidor es muy lento, ¿qué hago?

**R:**
1. **Upgrade a Starter** ($7/mes)
2. Usar **Redis para caché**
3. Optimizar queries a BD
4. Usar CDN (Cloudflare)

---

## 14. ¿Cómo monitorizas la aplicación?

**R:**
- Render Dashboard: CPU, RAM, requests
- Logs: Errores en tiempo real
- Uptime: https://status.render.com
- Alertas: Configurables en Settings

---

## 15. ¿Necesito cambiar código para producción?

**R:** Casi nada:
- ✓ DEBUG = False (hecho)
- ✓ SECURE_SSL_REDIRECT = True (hecho)
- ✓ ALLOWED_HOSTS (necesitas configurar)
- ✓ DATABASE_URL (necesitas configurar)
- ✓ SECRET_KEY (debe ser única)

---

## 16. ¿Puedo mantener dos versiones (staging + producción)?

**R:** Sí:
1. Crear dos servicios en Render
2. `main` branch → Producción
3. `staging` branch → Staging
4. Probar en staging antes de producción

---

## 17. ¿Cómo agrego variables de entorno sin redeploy?

**R:** En Render:
1. Dashboard → Settings → Environment
2. Modifica variable
3. Click Save
4. Render reinicia automáticamente (sin redeploy)

---

## 18. ¿Mi aplicación está protegida contra ataques?

**R:** SÍ, está configurada con:
- ✓ CSRF Protection
- ✓ SQL Injection Prevention (ORM Django)
- ✓ XSS Protection (plantillas)
- ✓ Rate Limiting (middleware)
- ✓ Input Sanitization (middleware)
- ✓ HTTPS Obligatorio (producción)
- ✓ Secure Cookies (HttpOnly, SameSite)

---

## 19. ¿Puedo usar Redis para sesiones?

**R:** Sí, agrega en settings.py:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL'),
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```

---

## 20. ¿Qué pasa si mi app crece mucho?

**R:** Opciones de escalabilidad:
1. Upgrade a plan Pro
2. Separar BD en instancia diferente
3. Usar load balancing
4. Migrar a AWS/Google Cloud

---

## 📞 Recursos Útiles

| Recurso | URL |
|---------|-----|
| Docs Render | https://render.com/docs |
| Django Docs | https://docs.djangoproject.com |
| Python-Decouple | https://github.com/henriquebastos/python-decouple |
| Gunicorn | https://gunicorn.org/ |
| WhiteNoise | http://whitenoise.evans.io/ |

---

## 🎯 Resumen

La aplicación ya está **100% preparada** para Render. Solo necesitas:

1. ✅ Git + GitHub (tu código)
2. ✅ Cuenta Render (hosting)
3. ✅ Configurar variables de entorno
4. ✅ ¡Desplegar!

**Tiempo total: ~30 minutos**

---

**¿Necesitas más ayuda?** Lee DEPLOYMENT_RENDER.md para instrucciones paso a paso.
