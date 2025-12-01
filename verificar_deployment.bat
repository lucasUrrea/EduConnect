@echo off
REM Script para preparar la aplicación para deployment en Render
REM Este script realiza verificaciones y prepara todo lo necesario

echo.
echo ================================================================================
echo  VERIFICACION DE DEPLOYMENT - EduConnect en Render
echo ================================================================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "manage.py" (
    echo ERROR: No se encontro manage.py
    echo Este script debe ejecutarse desde la raiz del proyecto Django
    pause
    exit /b 1
)

echo [1/7] Verificando requirements.txt...
if not exist "requirements.txt" (
    echo ERROR: requirements.txt no encontrado
    pause
    exit /b 1
)
echo OK: requirements.txt encontrado

echo [2/7] Verificando Procfile...
if not exist "Procfile" (
    echo ERROR: Procfile no encontrado
    pause
    exit /b 1
)
echo OK: Procfile encontrado

echo [3/7] Verificando runtime.txt...
if not exist "runtime.txt" (
    echo ERROR: runtime.txt no encontrado
    pause
    exit /b 1
)
echo OK: runtime.txt encontrado

echo [4/7] Verificando render.yaml...
if not exist "render.yaml" (
    echo ERROR: render.yaml no encontrado
    pause
    exit /b 1
)
echo OK: render.yaml encontrado

echo [5/7] Verificando .env.example...
if not exist ".env.example" (
    echo ERROR: .env.example no encontrado
    pause
    exit /b 1
)
echo OK: .env.example encontrado

echo [6/7] Verificando settings.py para produccion...
findstr /C:"config('DEBUG'" modulos_consultas\settings.py >nul
if %errorlevel% equ 0 (
    echo OK: settings.py configurado para variables de entorno
) else (
    echo WARNING: settings.py podria no estar completamente actualizado
)

echo [7/7] Verificando .gitignore...
if not exist ".gitignore" (
    echo WARNING: .gitignore no encontrado. Recomendado crear uno.
) else (
    echo OK: .gitignore encontrado
)

echo.
echo ================================================================================
echo  PROXIMO PASO
echo ================================================================================
echo.
echo 1. Asegurate de que Git esta inicializado:
echo    git init
echo    git add .
echo    git commit -m "Preparado para deployment"
echo.
echo 2. Crea un repositorio en GitHub y sube el codigo
echo.
echo 3. En Render.com:
echo    - Crea un nuevo Web Service
echo    - Conecta tu repositorio de GitHub
echo    - Configura las variables de entorno (ver .env.example)
echo    - Agrega una base de datos PostgreSQL
echo.
echo 4. Lee DEPLOYMENT_RENDER.md para instrucciones detalladas
echo.
echo ================================================================================
echo.
pause
