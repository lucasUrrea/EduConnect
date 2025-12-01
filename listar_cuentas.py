#!/usr/bin/env python
"""
Script para listar cuentas de estudiantes y docentes
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
os.environ['USE_SQLITE'] = '1'
django.setup()

from EduConnectApp.models import Usuarios, Estudiantes, Docentes

print("="*70)
print("👥 CUENTAS DE USUARIOS DEL SISTEMA")
print("="*70)
print()

# Obtener estudiantes
print("🎓 ESTUDIANTES:")
print("-" * 70)
estudiantes = Estudiantes.objects.select_related('id_usuario').all()
if estudiantes.exists():
    for est in estudiantes:
        usuario = est.id_usuario
        print(f"\n📧 Email: {usuario.email}")
        print(f"   Nombre: {usuario.nombre} {usuario.apellido_paterno}")
        print(f"   Matrícula: {est.numero_matricula}")
        print(f"   Carrera: {est.carrera or 'N/A'}")
        print(f"   Semestre: {est.semestre or 'N/A'}")
else:
    print("  No hay estudiantes registrados")

print("\n\n")

# Obtener docentes
print("👨‍🏫 DOCENTES:")
print("-" * 70)
docentes = Docentes.objects.select_related('id_usuario').all()
if docentes.exists():
    for doc in docentes:
        usuario = doc.id_usuario
        print(f"\n📧 Email: {usuario.email}")
        print(f"   Nombre: {usuario.nombre} {usuario.apellido_paterno}")
        print(f"   Código: {doc.codigo_docente}")
        print(f"   Departamento: {doc.departamento or 'N/A'}")
        print(f"   Título: {doc.titulo_academico or 'N/A'}")
else:
    print("  No hay docentes registrados")

print("\n\n")

# Administradores
print("👑 ADMINISTRADORES:")
print("-" * 70)
admins = Usuarios.objects.filter(tipo_usuario='admin')
if admins.exists():
    for admin in admins:
        print(f"\n📧 Email: {admin.email}")
        print(f"   Nombre: {admin.nombre} {admin.apellido_paterno}")
else:
    print("  No hay administradores registrados")

print("\n\n")
print("="*70)
print("ℹ️  NOTA: Para conocer las contraseñas, verifica los scripts")
print("   de creación de datos de prueba en la carpeta 'scripts/'")
print("="*70)
print()
print("🔐 Credenciales Admin conocidas:")
print("   Usuario: admin")
print("   Password: admin123")
print("="*70)
