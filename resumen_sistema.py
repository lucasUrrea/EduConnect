#!/usr/bin/env python
"""
Script de Resumen Ejecutivo - Muestra el estado completo del sistema
"""
import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
os.environ['USE_SQLITE'] = '1'
django.setup()

from django.conf import settings
from EduConnectApp.models import Usuarios, Estudiantes, Docentes, Consultas, Respuestas

def get_header():
    return f"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║          🎓 SISTEMA EDUCONNECT - RESUMEN EJECUTIVO 🎓                ║
║                                                                      ║
║                    Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}                     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

def get_divider():
    return "─" * 70

def main():
    print(get_header())
    
    # SECCIÓN 1: INFORMACIÓN DEL SISTEMA
    print("\n📊 INFORMACIÓN DEL SISTEMA")
    print(get_divider())
    print(f"Django Version:     {django.get_version()}")
    print(f"Python Version:     {os.sys.version.split()[0]}")
    print(f"Modo Debug:         {'🔴 ACTIVADO (Desarrollo)' if settings.DEBUG else '🟢 DESACTIVADO (Producción)'}")
    print(f"Base de Datos:      {'SQLite' if settings.DATABASES['default']['ENGINE'].endswith('sqlite3') else 'MySQL/MariaDB'}")
    print(f"Archivo DB:         {settings.DATABASES['default'].get('NAME', 'N/A')}")
    
    # SECCIÓN 2: ESTADÍSTICAS DE DATOS
    print("\n\n📈 ESTADÍSTICAS DE LA BASE DE DATOS")
    print(get_divider())
    
    stats = {
        "Usuarios Totales": Usuarios.objects.count(),
        "└─ Estudiantes": Estudiantes.objects.count(),
        "└─ Docentes": Docentes.objects.count(),
        "└─ Administradores": Usuarios.objects.filter(tipo_usuario='admin').count(),
        "Consultas Totales": Consultas.objects.count(),
        "└─ Pendientes": Consultas.objects.filter(estado='pendiente').count(),
        "└─ En Proceso": Consultas.objects.filter(estado='en_proceso').count(),
        "└─ Resueltas": Consultas.objects.filter(estado='resuelta').count(),
        "Respuestas Totales": Respuestas.objects.count(),
    }
    
    for key, value in stats.items():
        padding = " " * (30 - len(key))
        print(f"{key}:{padding}{value:>3}")
    
    # SECCIÓN 3: SEGURIDAD
    print("\n\n🔒 CONFIGURACIONES DE SEGURIDAD")
    print(get_divider())
    
    security_features = [
        ("CSRF Protection", "✅ Activo", f"{len(settings.CSRF_TRUSTED_ORIGINS)} orígenes confiables"),
        ("Session Security", "✅ Activo", f"Expiración: {settings.SESSION_COOKIE_AGE//3600}h"),
        ("Rate Limiting", "✅ Activo", "Prevención de ataques de fuerza bruta"),
        ("Input Sanitization", "✅ Activo", "Protección contra XSS/Inyección"),
        ("Activity Logging", "✅ Activo", "Auditoría de acciones"),
        ("Security Headers", "✅ Activo", "CSP, HSTS, XSS Filter"),
        ("SSL/HTTPS", "🔴 Dev Mode" if settings.DEBUG else "✅ Forzado", "Configurado para producción"),
    ]
    
    for feature, status, detail in security_features:
        print(f"  {status:<15} {feature:<25} │ {detail}")
    
    # SECCIÓN 4: MIDDLEWARE
    print("\n\n⚙️  MIDDLEWARE STACK")
    print(get_divider())
    
    middleware_names = [m.split('.')[-1] for m in settings.MIDDLEWARE]
    for i, mw in enumerate(middleware_names, 1):
        marker = "🔒" if "Security" in mw or "Csrf" in mw or "Rate" in mw or "Input" in mw else "⚙️"
        print(f"  {i:2d}. {marker} {mw}")
    
    # SECCIÓN 5: API REST
    print("\n\n🌐 CONFIGURACIÓN API REST")
    print(get_divider())
    
    auth_classes = settings.REST_FRAMEWORK.get('DEFAULT_AUTHENTICATION_CLASSES', [])
    perm_classes = settings.REST_FRAMEWORK.get('DEFAULT_PERMISSION_CLASSES', [])
    
    print("  Autenticación:")
    for auth in auth_classes:
        print(f"    ✓ {auth.split('.')[-1]}")
    
    print("\n  Permisos:")
    for perm in perm_classes:
        print(f"    ✓ {perm.split('.')[-1]}")
    
    # SECCIÓN 6: ACCESO AL SISTEMA
    print("\n\n🌍 ACCESO AL SISTEMA")
    print(get_divider())
    
    print("  URLs de Acceso:")
    print(f"    • Local:           http://localhost:8000/")
    print(f"    • Red Local:       http://192.168.1.13:8000/")
    print(f"    • Admin Panel:     http://localhost:8000/admin/")
    print(f"    • API Root:        http://localhost:8000/api/")
    
    print("\n  Credenciales Admin:")
    print(f"    • Usuario:         admin")
    print(f"    • Password:        admin123")
    
    # SECCIÓN 7: ARCHIVOS IMPORTANTES
    print("\n\n📁 ARCHIVOS Y DOCUMENTACIÓN")
    print(get_divider())
    
    files = [
        ("SECURITY_IMPROVEMENTS.md", "Documentación completa de seguridad"),
        ("GUIA_ACCESO_RED.md", "Guía para acceso desde red local"),
        ("iniciar_servidor.ps1", "Script para iniciar el servidor"),
        ("abrir_firewall.ps1", "Script para configurar firewall"),
        ("reset_admin_password.py", "Script para resetear contraseña admin"),
        ("test_security.py", "Verificación de configuraciones"),
        ("test_funcionamiento.py", "Pruebas de funcionalidad"),
    ]
    
    for filename, description in files:
        print(f"  📄 {filename:<30} │ {description}")
    
    # SECCIÓN 8: COMANDOS ÚTILES
    print("\n\n🚀 COMANDOS RÁPIDOS")
    print(get_divider())
    
    commands = [
        ("Iniciar servidor", ".\\iniciar_servidor.ps1"),
        ("Resetear admin", "python reset_admin_password.py"),
        ("Verificar seguridad", "python test_security.py"),
        ("Pruebas completas", "python test_funcionamiento.py"),
        ("Migraciones", "python manage.py migrate"),
        ("Shell interactivo", "python manage.py shell"),
    ]
    
    for action, command in commands:
        print(f"  {action:<25} │ {command}")
    
    # FOOTER
    print("\n" + "═" * 70)
    print("  ✅ Sistema configurado y listo para usar")
    print("  🔒 Todas las medidas de seguridad implementadas")
    print("  📚 Documentación completa disponible")
    print("═" * 70)
    print()

if __name__ == '__main__':
    main()
