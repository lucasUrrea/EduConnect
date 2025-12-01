DEV local rápido — EduConnect

Este archivo contiene notas rápidas para desarrolladores sobre cómo habilitar el modo compacto de desarrollo y cómo sembrar (seed) datos de prueba en la base SQLite usada para desarrollo local.

1) Habilitar `dev-compact` (modo compacto)

- Descripción: existe un conjunto de reglas CSS de "compactación" (espaciado reducido, tarjetas más pequeñas) que están intencionalmente aisladas en `static/EduConnectApp/css/overrides.css` bajo el prefijo `html.dev-compact`. Eso evita que afecten entornos de producción o a otros desarrolladores por accidente.

- Cómo usar:
  - Abre `EduConnectApp/templates/EduConnectApp/base.html` y añade la clase `dev-compact` al elemento `<html>` durante el desarrollo local. Ejemplo:

    <html class="dev-compact" lang="es">

  - Alternativamente, en DevTools puedes ejecutar:

    document.documentElement.classList.add('dev-compact')

  - Para desactivar, elimina la clase o recarga la página sin la clase.

2) Sembrar (seed) la base de datos SQLite para pruebas locales

- Descripción: varios scripts de `scripts/` preparan datos de ejemplo. El script recomendado para pruebas rápidas es `scripts/seed_example_data.py`.

- Comandos (Windows PowerShell, usando el virtualenv del proyecto):

    # Usar SQLite local durante esta sesión
    $env:USE_SQLITE='1'

    # Opcional: asegurar que el directorio de trabajo esté en PYTHONPATH (PowerShell):
    $env:PYTHONPATH=(Get-Location).Path

    # Ejecutar el script de seed
    .\.venv\Scripts\python scripts/seed_example_data.py

- Resultado esperado: el script imprimirá "Seeding complete" y la base de datos `db.sqlite3` (en el directorio raíz del proyecto) contendrá usuarios, asignaturas, una consulta y una respuesta de ejemplo.

3) Ejecutar el servidor de desarrollo con SQLite

- Usar el siguiente comando en PowerShell para iniciar el servidor en 127.0.0.1:8000 y forzar uso de SQLite en la sesión:

    $env:USE_SQLITE='1'; .\.venv\Scripts\python manage.py runserver 127.0.0.1:8000

- Nota: si prefieres usar MariaDB/MySQL en local, exporta las variables de entorno `DB_NAME`, `DB_USER`, `DB_PASS`, `DB_HOST`, `DB_PORT` y asegúrate de tener `mysqlclient>=1.4.3` instalado en el virtualenv.

4) Probar endpoints clave rápidamente (PowerShell)

    $env:USE_SQLITE='1'; (Invoke-WebRequest -Uri http://127.0.0.1:8000/ -UseBasicParsing).StatusCode
    $env:USE_SQLITE='1'; (Invoke-WebRequest -Uri http://127.0.0.1:8000/login/ -UseBasicParsing).StatusCode

5) Notas adicionales

- Los antiguos backups de CSS con reglas muy grandes para `body` (padding-top: 90px / 140px) han sido neutralizados en `.comment_backups/` para evitar confusiones. Si necesitas recuperar algo, revisa los archivos allí.
- Para tests automatizados hay varios scripts en `tmp/` que se usaron durante depuración (`tmp/run_page_checks.py`, `tmp/test_responder.py`, `tmp/debug_views.py`).

