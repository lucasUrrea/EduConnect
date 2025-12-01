#!/usr/bin/env python
"""
Script para verificar y arreglar cuentas de usuarios
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
os.environ['USE_SQLITE'] = '1'
django.setup()

from django.contrib.auth import get_user_model, authenticate
from EduConnectApp.models import Usuarios, Estudiantes, Docentes

User = get_user_model()

print("="*70)
print("🔧 VERIFICACIÓN Y REPARACIÓN DE CUENTAS")
print("="*70)
print()

# Lista de usuarios a verificar y reparar
usuarios_config = [
    # Estudiantes
    {'email': 'student1@example.com', 'password': 'studpass', 'tipo': 'estudiante'},
    {'email': 'teststudent@example.com', 'password': 'testpass', 'tipo': 'estudiante'},
    {'email': 'stud_live1@example.com', 'password': 'studpass', 'tipo': 'estudiante'},
    {'email': 'stud_live2@example.com', 'password': 'studpass', 'tipo': 'estudiante'},
    {'email': 'stud_live3@example.com', 'password': 'studpass', 'tipo': 'estudiante'},
    # Docentes
    {'email': 'docente1@example.com', 'password': 'docpass', 'tipo': 'docente'},
    {'email': 'doc_live1@example.com', 'password': 'docpass', 'tipo': 'docente'},
    {'email': 'doc_live2@example.com', 'password': 'docpass', 'tipo': 'docente'},
    {'email': 'doc_live3@example.com', 'password': 'docpass', 'tipo': 'docente'},
]

print("🔍 VERIFICANDO Y REPARANDO USUARIOS...")
print("-" * 70)

reparados = 0
errores = 0

for config in usuarios_config:
    email = config['email']
    password = config['password']
    tipo = config['tipo']
    
    print(f"\n📧 {email}")
    
    try:
        # Verificar en tabla Usuarios
        try:
            usuario = Usuarios.objects.get(email=email)
            print(f"   ✓ Existe en Usuarios")
            
            # Verificar y actualizar estado
            if usuario.estado != 'activo':
                usuario.estado = 'activo'
                usuario.save()
                print(f"   ✓ Estado actualizado a 'activo'")
        except Usuarios.DoesNotExist:
            print(f"   ✗ NO existe en tabla Usuarios")
            continue
        
        # Verificar/crear usuario Django
        try:
            django_user = User.objects.get(username=email)
            print(f"   ✓ Usuario Django existe")
        except User.DoesNotExist:
            # Crear usuario Django
            django_user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            print(f"   ✓ Usuario Django creado")
        
        # Actualizar contraseña
        django_user.set_password(password)
        django_user.is_active = True
        django_user.save()
        print(f"   ✓ Contraseña actualizada")
        print(f"   ✓ Usuario activado")
        
        # Probar autenticación
        test_auth = authenticate(username=email, password=password)
        if test_auth:
            print(f"   ✅ AUTENTICACIÓN EXITOSA")
            reparados += 1
        else:
            print(f"   ❌ Error en autenticación")
            errores += 1
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        errores += 1

print("\n\n" + "="*70)
print("📊 RESUMEN")
print("="*70)
print(f"✅ Usuarios reparados: {reparados}")
print(f"❌ Errores: {errores}")
print()

# Mostrar credenciales actualizadas
print("🔐 CREDENCIALES ACTUALIZADAS:")
print("-" * 70)
print("\n👑 ADMIN:")
print("   Usuario: admin")
print("   Password: admin123")
print("\n🎓 ESTUDIANTES:")
print("   student1@example.com / studpass")
print("   teststudent@example.com / testpass")
print("   stud_live1-3@example.com / studpass")
print("\n👨‍🏫 DOCENTES:")
print("   docente1@example.com / docpass")
print("   doc_live1-3@example.com / docpass")
print()
print("="*70)
print("✅ Ahora puedes intentar iniciar sesión nuevamente")
print("="*70)
