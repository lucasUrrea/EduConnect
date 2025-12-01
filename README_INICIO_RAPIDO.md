# 🎓 Sistema EduConnect - Guía de Inicio Rápido

## 📋 Resumen Ejecutivo

Sistema Django completo con **todas las medidas de seguridad implementadas**:
- ✅ Protección CSRF
- ✅ Configuración SSL/HTTPS
- ✅ Rate Limiting
- ✅ Input Sanitization  
- ✅ Activity Logging
- ✅ Serializers optimizados
- ✅ Validaciones completas

---

## 🚀 Inicio Rápido (3 pasos)

### 1️⃣ Ver Estado del Sistema
```powershell
python resumen_sistema.py
```

### 2️⃣ Iniciar Servidor
```powershell
.\iniciar_servidor.ps1
```

### 3️⃣ Acceder
- **Web:** http://localhost:8000/
- **Admin:** http://localhost:8000/admin/
  - Usuario: `admin`
  - Password: `admin123`

---

## 🧪 Scripts de Prueba

### Verificar Seguridad
```powershell
python test_security.py
```
Muestra todas las configuraciones de seguridad activas.

### Pruebas de Funcionamiento
```powershell
python test_funcionamiento.py
```
Ejecuta pruebas completas:
- Autenticación
- Base de datos
- Validaciones de serializers
- Protección de campos sensibles
- Configuraciones de seguridad

### Resumen del Sistema
```powershell
python resumen_sistema.py
```
Vista ejecutiva completa del estado del sistema.

---

## 🔐 Gestión de Usuarios

### Resetear Contraseña Admin
```powershell
python reset_admin_password.py
```
Resetea las credenciales a:
- Usuario: `admin`
- Password: `admin123`

### Crear Nuevo Superusuario
```powershell
python manage.py createsuperuser --username <usuario> --email <email>
```

---

## 🌐 Acceso desde Red Local

### Para acceder desde otras computadoras:

1. **Primera vez: Abrir Firewall** (como Administrador)
   ```powershell
   .\abrir_firewall.ps1
   ```

2. **Iniciar servidor**
   ```powershell
   .\iniciar_servidor.ps1
   ```

3. **Acceder desde otra PC**
   ```
   http://192.168.1.13:8000/
   ```
   (Reemplaza `192.168.1.13` con tu IP local)

4. **Obtener tu IP**
   ```powershell
   ipconfig
   ```
   Busca "Dirección IPv4" en tu adaptador de red activo.

---

## 📊 Comandos Django Útiles

### Base de Datos
```powershell
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Shell interactivo
python manage.py shell
```

### Servidor
```powershell
# Iniciar servidor (solo local)
python manage.py runserver

# Iniciar servidor (red local)
python manage.py runserver 0.0.0.0:8000
```

### Datos
```powershell
# Crear backup
python manage.py dumpdata > backup.json

# Cargar datos
python manage.py loaddata backup.json
```

---

## 📁 Estructura de Archivos Clave

```
Modulos de consultas/
├── 📄 resumen_sistema.py              # ⭐ Resumen ejecutivo
├── 📄 test_security.py                # ⭐ Verificar seguridad
├── 📄 test_funcionamiento.py          # ⭐ Pruebas completas
├── 📄 iniciar_servidor.ps1            # ⭐ Iniciar servidor
├── 📄 abrir_firewall.ps1              # Configurar firewall
├── 📄 reset_admin_password.py         # Resetear admin
├── 📄 SECURITY_IMPROVEMENTS.md        # 📚 Documentación seguridad
├── 📄 GUIA_ACCESO_RED.md              # 📚 Guía de red local
├── 📄 README_INICIO_RAPIDO.md         # 📚 Esta guía
├── 📄 manage.py                       # Django management
├── 📄 db.sqlite3                      # Base de datos SQLite
├── modulos_consultas/
│   ├── settings.py                    # 🔒 Config. seguridad
│   └── urls.py
└── EduConnectApp/
    ├── models.py                      # Modelos de datos
    ├── views.py                       # Vistas
    ├── middleware.py                  # 🔒 Middleware seguridad
    └── api/
        └── serializers.py             # 🔒 Serializers mejorados
```

---

## 🔒 Mejoras de Seguridad Implementadas

### 1. CSRF Protection
- Tokens CSRF en todas las peticiones POST/PUT/DELETE
- Orígenes confiables configurados
- Cookies seguras en producción

### 2. SSL/HTTPS (Producción)
- Redirección automática a HTTPS
- HSTS habilitado (1 año)
- Cookies solo via HTTPS

### 3. Rate Limiting
- Login: 5 intentos / minuto
- API: 50 requests / minuto
- General: 100 requests / minuto

### 4. Input Sanitization
- Detección de scripts maliciosos
- Prevención de XSS
- Validación de inputs

### 5. Activity Logging
- Registro de todas las acciones importantes
- IP y User-Agent capturados
- Auditoría completa

### 6. Serializers Optimizados
- Campos read_only / write_only
- Validaciones personalizadas
- Nunca expone passwords
- Mensajes de error claros

**Ver documentación completa:** `SECURITY_IMPROVEMENTS.md`

---

## 🛠️ Configuración de Entorno

### Desarrollo (Actual)
```python
DEBUG = True
USE_SQLITE = '1'
ALLOWED_HOSTS = ['*']
```

### Producción (Recomendado)
```python
DEBUG = False
USE_SQLITE = '0'  # Usar MySQL/MariaDB
ALLOWED_HOSTS = ['tudominio.com', 'www.tudominio.com']
```

Variables de entorno para producción:
```bash
DB_NAME=educonnect_db
DB_USER=usuario_seguro
DB_PASSWORD=password_complejo
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=tu-secret-key-muy-seguro
```

---

## 📚 Documentación Adicional

| Archivo | Descripción |
|---------|-------------|
| `SECURITY_IMPROVEMENTS.md` | Documentación completa de seguridad |
| `GUIA_ACCESO_RED.md` | Guía para acceso desde red local |
| `DEV_NOTES.md` | Notas de desarrollo |
| `README.md` | README original del proyecto |

---

## 🆘 Solución de Problemas

### Error: "Credenciales inválidas"
```powershell
python reset_admin_password.py
```

### Error: "Puerto 8000 en uso"
```powershell
# Buscar proceso
Get-Process | Where-Object {$_.ProcessName -eq "python"}

# Matar proceso
Stop-Process -Id <PID>
```

### Error: "No se puede conectar desde otra PC"
1. Verificar que el firewall esté abierto:
   ```powershell
   Get-NetFirewallRule -DisplayName "*Django*"
   ```
2. Ejecutar como administrador:
   ```powershell
   .\abrir_firewall.ps1
   ```

### Error de migraciones
```powershell
python manage.py migrate --run-syncdb
```

---

## 💡 Tips y Mejores Prácticas

### Desarrollo
- ✅ Usa `iniciar_servidor.ps1` para inicio rápido
- ✅ Ejecuta `test_funcionamiento.py` después de cambios
- ✅ Revisa logs en `LogsActividad` para debugging

### Producción
- ⚠️ Cambia `DEBUG = False`
- ⚠️ Usa base de datos MySQL/PostgreSQL
- ⚠️ Configura `ALLOWED_HOSTS` específicamente
- ⚠️ Usa variables de entorno para secretos
- ⚠️ Habilita HTTPS con certificado SSL
- ⚠️ Configura backups automáticos

### Seguridad
- 🔒 Revisa logs regularmente
- 🔒 Actualiza Django periódicamente
- 🔒 Monitorea rate limits
- 🔒 Usa contraseñas fuertes en producción

---

## 📞 Comandos de Emergencia

### Resetear Todo
```powershell
# Borrar base de datos
Remove-Item db.sqlite3

# Recrear migraciones
python manage.py migrate

# Crear admin
python reset_admin_password.py
```

### Ver Logs en Tiempo Real
```powershell
# En Python
python manage.py shell
>>> from EduConnectApp.models import LogsActividad
>>> LogsActividad.objects.order_by('-fecha_evento')[:10]
```

---

## ✅ Checklist de Inicio

- [ ] Ejecutar `python resumen_sistema.py`
- [ ] Verificar que todo esté OK
- [ ] Abrir firewall (primera vez)
- [ ] Iniciar servidor con `.\iniciar_servidor.ps1`
- [ ] Acceder a http://localhost:8000/
- [ ] Login en /admin/ con admin/admin123
- [ ] Probar funcionalidad básica
- [ ] Verificar acceso desde otra PC (si aplica)

---

## 🎯 Próximos Pasos

1. **Explorar el sistema**
   - Panel de administración
   - API REST endpoints
   - Funcionalidad de consultas

2. **Personalizar**
   - Ajustar configuraciones en `settings.py`
   - Modificar límites de rate limiting
   - Personalizar validaciones

3. **Preparar para producción**
   - Configurar base de datos MySQL
   - Obtener certificado SSL
   - Configurar servidor web (Nginx/Apache)
   - Configurar monitoreo

---

**¡Sistema listo para usar! 🚀**

Para más información, consulta la documentación completa en los archivos .md
