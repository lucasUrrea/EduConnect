# Script para iniciar el servidor Django accesible desde la red local
# Autor: GitHub Copilot
# Fecha: 2025-11-04

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Servidor Django - Acceso en Red Local" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configurar SQLite
$env:USE_SQLITE='1'

# Obtener IP local
$LocalIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*"} | Select-Object -First 1).IPAddress

if ($LocalIP) {
    Write-Host "Tu IP local es: " -NoNewline -ForegroundColor Yellow
    Write-Host $LocalIP -ForegroundColor Green
    Write-Host ""
    Write-Host "URLs de acceso:" -ForegroundColor Yellow
    Write-Host "  - Desde esta PC:      http://localhost:8000/" -ForegroundColor White
    Write-Host "  - Desde esta PC:      http://127.0.0.1:8000/" -ForegroundColor White
    Write-Host "  - Desde otra PC:      http://$LocalIP`:8000/" -ForegroundColor Green
    Write-Host "  - Panel Admin:        http://$LocalIP`:8000/admin/" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "No se pudo detectar la IP local automáticamente" -ForegroundColor Red
    Write-Host "Ejecuta 'ipconfig' para ver tu dirección IP" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Credenciales de Admin:" -ForegroundColor Yellow
Write-Host "  Usuario: admin" -ForegroundColor White
Write-Host "  Password: (la que configuraste)" -ForegroundColor White
Write-Host ""

Write-Host "Verificando regla de firewall..." -ForegroundColor Yellow
$firewallRule = Get-NetFirewallRule -DisplayName "Django Development Server" -ErrorAction SilentlyContinue

if (-not $firewallRule) {
    Write-Host "Creando regla de firewall para permitir conexiones entrantes..." -ForegroundColor Yellow
    try {
        New-NetFirewallRule -DisplayName "Django Development Server" `
                            -Direction Inbound `
                            -Protocol TCP `
                            -LocalPort 8000 `
                            -Action Allow `
                            -Profile Private,Domain `
                            -ErrorAction Stop | Out-Null
        Write-Host "✓ Regla de firewall creada exitosamente" -ForegroundColor Green
    } catch {
        Write-Host "⚠ No se pudo crear la regla de firewall automáticamente" -ForegroundColor Red
        Write-Host "  Ejecuta PowerShell como Administrador para permitir conexiones" -ForegroundColor Yellow
    }
    Write-Host ""
} else {
    Write-Host "✓ Regla de firewall ya existe" -ForegroundColor Green
    Write-Host ""
}

Write-Host "Iniciando servidor Django..." -ForegroundColor Yellow
Write-Host "Presiona CTRL+C para detener el servidor" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio correcto
Set-Location "c:\Users\lucas\OneDrive\Escritorio\Modulos de consultas\Modulos de consultas"

# Iniciar servidor
& "C:/Users/lucas/OneDrive/Escritorio/Modulos de consultas/.venv/Scripts/python.exe" manage.py runserver 0.0.0.0:8000
