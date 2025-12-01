# Script para abrir el firewall de Windows para Django
# IMPORTANTE: Este script debe ejecutarse como ADMINISTRADOR

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Configuración de Firewall para Django" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si se ejecuta como administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠ ERROR: Este script requiere privilegios de Administrador" -ForegroundColor Red
    Write-Host ""
    Write-Host "Cómo ejecutar como Administrador:" -ForegroundColor Yellow
    Write-Host "1. Haz clic derecho en PowerShell" -ForegroundColor White
    Write-Host "2. Selecciona 'Ejecutar como administrador'" -ForegroundColor White
    Write-Host "3. Ejecuta este comando:" -ForegroundColor White
    Write-Host "   cd 'c:\Users\lucas\OneDrive\Escritorio\Modulos de consultas\Modulos de consultas'" -ForegroundColor Cyan
    Write-Host "   .\abrir_firewall.ps1" -ForegroundColor Cyan
    Write-Host ""
    pause
    exit 1
}

Write-Host "Verificando regla de firewall existente..." -ForegroundColor Yellow
$existingRule = Get-NetFirewallRule -DisplayName "Django Development Server Port 8000" -ErrorAction SilentlyContinue

if ($existingRule) {
    Write-Host "✓ La regla ya existe. Eliminando para recrear..." -ForegroundColor Yellow
    Remove-NetFirewallRule -DisplayName "Django Development Server Port 8000"
}

Write-Host "Creando regla de firewall para puerto 8000..." -ForegroundColor Yellow

try {
    New-NetFirewallRule -DisplayName "Django Development Server Port 8000" `
                        -Description "Permite conexiones entrantes al servidor de desarrollo Django" `
                        -Direction Inbound `
                        -Protocol TCP `
                        -LocalPort 8000 `
                        -Action Allow `
                        -Profile Private,Domain `
                        -Enabled True | Out-Null
    
    Write-Host ""
    Write-Host "✓ ¡Regla de firewall creada exitosamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "El puerto 8000 ahora está abierto para conexiones de red local" -ForegroundColor Green
    Write-Host ""
    
    # Mostrar la regla creada
    Write-Host "Detalles de la regla creada:" -ForegroundColor Yellow
    Get-NetFirewallRule -DisplayName "Django Development Server Port 8000" | Format-Table DisplayName, Enabled, Direction, Action
    
} catch {
    Write-Host ""
    Write-Host "✗ Error al crear la regla de firewall:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    exit 1
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Ahora puedes ejecutar: .\iniciar_servidor.ps1" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
pause
