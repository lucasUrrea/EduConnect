# Script para iniciar el servidor Django accesible desde la red local
# Ejecutar como: .\iniciar_servidor_red.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Iniciando EduConnect Server (Red Local)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Obtener la IP local
$ip = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi" -ErrorAction SilentlyContinue).IPAddress
if (-not $ip) {
    $ip = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Ethernet" -ErrorAction SilentlyContinue).IPAddress
}

if ($ip) {
    Write-Host "Tu IP local es: " -NoNewline
    Write-Host "$ip" -ForegroundColor Green
    Write-Host ""
    Write-Host "Otras computadoras pueden acceder en:" -ForegroundColor Yellow
    Write-Host "  http://$ip:8000" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "No se pudo detectar la IP local automáticamente" -ForegroundColor Yellow
    Write-Host "Ejecuta 'ipconfig' para encontrar tu dirección IPv4" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Acceso local también disponible en:" -ForegroundColor Yellow
Write-Host "  http://localhost:8000" -ForegroundColor Green
Write-Host "  http://127.0.0.1:8000" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona CTRL+C para detener el servidor" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configurar variable de entorno para usar SQLite
$env:USE_SQLITE = '1'

# Iniciar el servidor
python manage.py runserver 0.0.0.0:8000
