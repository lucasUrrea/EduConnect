# 🚀 Guía Rápida: Acceder al Servidor Django desde la Red Local

## 📋 Problema Común
Si no puedes acceder al servidor Django desde otra computadora, probablemente es por el **firewall de Windows** que bloquea el puerto 8000.

## ✅ Solución Paso a Paso

### Paso 1: Abrir el Firewall (SOLO UNA VEZ)
Ejecuta PowerShell **COMO ADMINISTRADOR**:

1. Busca "PowerShell" en el menú inicio
2. Haz clic derecho → "Ejecutar como administrador"
3. Ejecuta este comando (copia y pega TODO en una línea):

```powershell
netsh advfirewall firewall add rule name="Django Development Server" dir=in action=allow protocol=TCP localport=8000
```

**Alternativa:** Si prefieres usar el script, ejecuta:
```powershell
cd "c:\Users\lucas\OneDrive\Escritorio\Modulos de consultas\Modulos de consultas"; .\abrir_firewall.ps1
```

✅ Deberías ver el mensaje: "Correcto."

Esto abrirá el puerto 8000 en el firewall de Windows.

### Paso 2: Iniciar el Servidor
En cualquier PowerShell (no requiere privilegios de admin):

```powershell
cd "c:\Users\lucas\OneDrive\Escritorio\Modulos de consultas\Modulos de consultas"
.\iniciar_servidor.ps1
```

Este script:
- ✓ Detecta automáticamente tu IP local
- ✓ Muestra las URLs de acceso
- ✓ Inicia el servidor Django en modo red

### Paso 3: Acceder desde Otra Computadora

**Tu IP local actual:** `192.168.1.13`

Desde otra computadora en la misma red WiFi, abre un navegador y ve a:
- **Página principal:** `http://192.168.1.13:8000/`
- **Panel Admin:** `http://192.168.1.13:8000/admin/`

**Credenciales de Admin:**
- Usuario: `admin`
- Password: (la que configuraste)

---

## 🔧 Método Manual (Si los scripts no funcionan)

### 1. Abrir Firewall Manualmente

En PowerShell como **Administrador** (ejecuta UNO de estos comandos):

**Opción 1 - Comando directo (MÁS FÁCIL):**
```powershell
netsh advfirewall firewall add rule name="Django Development Server" dir=in action=allow protocol=TCP localport=8000
```

**Opción 2 - PowerShell moderno:**
```powershell
New-NetFirewallRule -DisplayName "Django Port 8000" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow -Profile Private,Domain
```

### 2. Iniciar Servidor Manualmente

En PowerShell normal:
```powershell
cd "c:\Users\lucas\OneDrive\Escritorio\Modulos de consultas\Modulos de consultas"
$env:USE_SQLITE='1'
& "C:/Users/lucas/OneDrive/Escritorio/Modulos de consultas/.venv/Scripts/python.exe" manage.py runserver 0.0.0.0:8000
```

### 3. Obtener tu IP Local

```powershell
ipconfig
```
Busca "Dirección IPv4" de tu adaptador WiFi o Ethernet (generalmente empieza con 192.168.x.x)

---

## 🔍 Verificar que Funciona

### Desde Tu PC:
1. Abre: `http://localhost:8000/`
2. Si funciona aquí, el servidor está OK

### Desde Otra PC:
1. Verifica que ambas PCs están en la **misma red WiFi**
2. Abre: `http://192.168.1.13:8000/` (usa tu IP)
3. Si dice "No se puede acceder", revisa el firewall

---

## ❓ Troubleshooting

### "No se puede conectar al sitio"
- ✓ Verifica que el servidor esté corriendo (debe decir "Starting development server...")
- ✓ Asegúrate de que ambas PCs están en la misma red WiFi
- ✓ Ejecuta el script `abrir_firewall.ps1` como administrador
- ✓ Desactiva temporalmente el antivirus para probar

### "Tu IP cambió"
Si reinicias el router o cambias de red, tu IP puede cambiar. Ejecuta:
```powershell
ipconfig
```
Y usa la nueva IP.

### Verificar Firewall
Para ver si la regla del firewall existe:
```powershell
Get-NetFirewallRule -DisplayName "*Django*"
```

---

## 📝 Notas Importantes

⚠ **Solo para Desarrollo**: Esta configuración es para desarrollo local. NO usar en producción.

⚠ **Seguridad**: `ALLOWED_HOSTS = ['*']` permite cualquier host. Después de probar, puedes limitarlo a IPs específicas en `settings.py`.

⚠ **Red Local**: Solo funcionará en tu red local (WiFi/Ethernet). No es accesible desde Internet.

---

## 🎯 Resumen Rápido

```powershell
# 1. PRIMERA VEZ: Abrir firewall (como Admin)
.\abrir_firewall.ps1

# 2. SIEMPRE: Iniciar servidor
.\iniciar_servidor.ps1

# 3. Acceder desde otra PC
# http://192.168.1.13:8000/
```

¡Listo! 🎉
