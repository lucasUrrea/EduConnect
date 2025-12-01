# ========================================
# SCRIPT DE INICIO - EDUCONNECT PROFESIONAL
# ========================================

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "║    🎓 EDUCONNECT - PLATAFORMA ACADÉMICA PROFESIONAL       ║" -ForegroundColor Cyan
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Configurar variable de entorno para SQLite
$env:USE_SQLITE = '1'
Write-Host "✅ Configurado: Usando SQLite (desarrollo)" -ForegroundColor Green

# Obtener IP local
Write-Host ""
Write-Host "🔍 Detectando dirección IP local..." -ForegroundColor Yellow

try {
    $localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" } | Select-Object -First 1).IPAddress
    
    if ($localIP) {
        Write-Host "📡 IP Local detectada: $localIP" -ForegroundColor Green
    } else {
        $localIP = "127.0.0.1"
        Write-Host "⚠️  No se detectó IP de red, usando localhost" -ForegroundColor Yellow
    }
} catch {
    $localIP = "127.0.0.1"
    Write-Host "⚠️  Error al detectar IP, usando localhost" -ForegroundColor Yellow
}

# Mostrar información de acceso
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║  🌐 ACCESO A LA PLATAFORMA                                 ║" -ForegroundColor Magenta
Write-Host "╠════════════════════════════════════════════════════════════╣" -ForegroundColor Magenta
Write-Host "║                                                            ║" -ForegroundColor Magenta
Write-Host "║  🖥️  Localhost:                                            ║" -ForegroundColor Magenta
Write-Host "║      http://localhost:8000/                                ║" -ForegroundColor White
Write-Host "║      http://127.0.0.1:8000/                                ║" -ForegroundColor White
Write-Host "║                                                            ║" -ForegroundColor Magenta

if ($localIP -ne "127.0.0.1") {
    Write-Host "║  🌍 Red Local:                                             ║" -ForegroundColor Magenta
    Write-Host "║      http://${localIP}:8000/                                 ║" -ForegroundColor White
    Write-Host "║                                                            ║" -ForegroundColor Magenta
}

Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta

# Mostrar páginas disponibles
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  📄 PÁGINAS DISPONIBLES                                    ║" -ForegroundColor Cyan
Write-Host "╠════════════════════════════════════════════════════════════╣" -ForegroundColor Cyan
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "║  🏠 Home (Landing)            /                            ║" -ForegroundColor White
Write-Host "║  🔐 Login                     /login/                      ║" -ForegroundColor White
Write-Host "║  👨‍🎓 Dashboard Estudiante      /dashboard/estudiante/      ║" -ForegroundColor White
Write-Host "║  👨‍🏫 Dashboard Docente          /dashboard/docente/         ║" -ForegroundColor White
Write-Host "║  ➕ Crear Consulta            /consultas/crear/            ║" -ForegroundColor White
Write-Host "║  📋 Mis Consultas             /consultas/mis/              ║" -ForegroundColor White
Write-Host "║  🔧 Admin Django              /admin/                      ║" -ForegroundColor White
Write-Host "║  🚀 API REST                  /api/                        ║" -ForegroundColor White
Write-Host "║  📚 API Docs (Swagger)        /api/docs/                   ║" -ForegroundColor White
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# Mostrar credenciales
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  🔑 CREDENCIALES DE ACCESO                                 ║" -ForegroundColor Green
Write-Host "╠════════════════════════════════════════════════════════════╣" -ForegroundColor Green
Write-Host "║                                                            ║" -ForegroundColor Green
Write-Host "║  👤 Admin:                                                 ║" -ForegroundColor Green
Write-Host "║     Email:    admin@educonnect.com                         ║" -ForegroundColor White
Write-Host "║     Password: admin123                                     ║" -ForegroundColor White
Write-Host "║                                                            ║" -ForegroundColor Green
Write-Host "║  👨‍🎓 Estudiante de prueba:                                  ║" -ForegroundColor Green
Write-Host "║     Email:    joseph.rivera@estudiante.com                 ║" -ForegroundColor White
Write-Host "║     Password: studpass                                     ║" -ForegroundColor White
Write-Host "║                                                            ║" -ForegroundColor Green
Write-Host "║  👨‍🏫 Docente de prueba:                                      ║" -ForegroundColor Green
Write-Host "║     Email:    maria.lopez@docente.com                      ║" -ForegroundColor White
Write-Host "║     Password: docpass                                      ║" -ForegroundColor White
Write-Host "║                                                            ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green

# Mostrar características del diseño
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║  ✨ DISEÑO PROFESIONAL IMPLEMENTADO                        ║" -ForegroundColor Yellow
Write-Host "╠════════════════════════════════════════════════════════════╣" -ForegroundColor Yellow
Write-Host "║                                                            ║" -ForegroundColor Yellow
Write-Host "║  ✅ Sistema de diseño completo con variables CSS           ║" -ForegroundColor White
Write-Host "║  ✅ Animaciones suaves en todos los elementos              ║" -ForegroundColor White
Write-Host "║  ✅ Navbar glassmorphism con backdrop-filter               ║" -ForegroundColor White
Write-Host "║  ✅ Cards con hover effects y gradientes                   ║" -ForegroundColor White
Write-Host "║  ✅ Botones con animaciones de onda                        ║" -ForegroundColor White
Write-Host "║  ✅ Hero section con gradientes animados                   ║" -ForegroundColor White
Write-Host "║  ✅ Stats cards con contadores JavaScript                  ║" -ForegroundColor White
Write-Host "║  ✅ Login card flotante con efectos premium                ║" -ForegroundColor White
Write-Host "║  ✅ 100% responsive (desktop, tablet, mobile)              ║" -ForegroundColor White
Write-Host "║  ✅ Paleta de colores profesional (15+ colores)            ║" -ForegroundColor White
Write-Host "║  ✅ Sistema de sombras con profundidad (7 niveles)         ║" -ForegroundColor White
Write-Host "║  ✅ Tipografía Inter con escalas responsive                ║" -ForegroundColor White
Write-Host "║                                                            ║" -ForegroundColor Yellow
Write-Host "║  📚 Ver documentación completa en:                         ║" -ForegroundColor Yellow
Write-Host "║     - DISEÑO_PROFESIONAL.md                                ║" -ForegroundColor White
Write-Host "║     - RESUMEN_DISEÑO.md                                    ║" -ForegroundColor White
Write-Host "║                                                            ║" -ForegroundColor Yellow
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow

# Preguntar si desea continuar
Write-Host ""
Write-Host "🚀 ¿Deseas iniciar el servidor ahora? (S/N): " -ForegroundColor Cyan -NoNewline
$respuesta = Read-Host

if ($respuesta -eq 'S' -or $respuesta -eq 's' -or $respuesta -eq 'Y' -or $respuesta -eq 'y' -or $respuesta -eq '') {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║  🚀 INICIANDO SERVIDOR DJANGO...                           ║" -ForegroundColor Magenta
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "⏳ Espera unos segundos mientras el servidor se inicia..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "💡 Presiona Ctrl+C para detener el servidor" -ForegroundColor Cyan
    Write-Host ""
    
    # Iniciar servidor
    python manage.py runserver 0.0.0.0:8000
    
} else {
    Write-Host ""
    Write-Host "❌ Operación cancelada" -ForegroundColor Red
    Write-Host ""
    Write-Host "Para iniciar el servidor manualmente, ejecuta:" -ForegroundColor Yellow
    Write-Host "  `$env:USE_SQLITE='1' ; python manage.py runserver 0.0.0.0:8000" -ForegroundColor White
    Write-Host ""
}
