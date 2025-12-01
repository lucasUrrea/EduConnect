# 🔐 CREDENCIALES DE ACCESO AL SISTEMA

**Última actualización:** 04/11/2025 22:30

---

## 👑 ADMINISTRADOR

**Panel de Admin Django:**
```
URL:           http://localhost:8000/admin/
Username:      admin@example.com
Password:      admin123
(Usa el email como username)
```

**Administrador Web (Acceso a la aplicación):**
```
Email:    admin@educonnect.com
Password: admin123
Nombre:   Admin Sistema
Tipo:     Administrador
```

---

## 🎓 ESTUDIANTES

### Estudiante Principal
```
Email:    student1@example.com
Password: studpass
Nombre:   Joseph Nohra
Matrícula: STU0001
```

### Estudiante de Prueba
```
Email:    teststudent@example.com
Password: testpass
Nombre:   Test Student
Matrícula: MAT0001
```

### Estudiantes Live (1-10)
```
Email:    stud_live1@example.com
          stud_live2@example.com
          stud_live3@example.com
          ... hasta stud_live10@example.com
Password: studpass (todos)
Nombres:  Student1 Live, Student2 Live, etc.
```

---

## 👨‍🏫 DOCENTES

### Docente Principal
```
Email:    docente1@example.com
Password: docpass
Nombre:   Sebastian Pizarro
Código:   DOC001
```

### Docentes Live (1-3)
```
Email:    doc_live1@example.com
          doc_live2@example.com
          doc_live3@example.com
Password: docpass (todos)
Nombres:  Doc1 Live, Doc2 Live, Doc3 Live
```

---

## 🌐 URLs DE ACCESO

### Desde tu PC:
- **Login:** http://localhost:8000/login/
- **Admin:** http://localhost:8000/admin/
- **Home:** http://localhost:8000/

### Desde otra PC en la red:
- **Login:** http://192.168.1.13:8000/login/
- **Admin:** http://192.168.1.13:8000/admin/
- **Home:** http://192.168.1.13:8000/

---

## ✅ ESTADO DE LAS CUENTAS

Todas las cuentas han sido verificadas y reparadas el 04/11/2025:
- ✅ 9 usuarios verificados
- ✅ Contraseñas actualizadas
- ✅ Usuarios activados
- ✅ Autenticación probada y funcionando

---

## 🔧 COMANDOS ÚTILES

### Resetear contraseña del admin:
```powershell
python reset_admin_password.py
```

### Reparar todas las cuentas:
```powershell
python reparar_cuentas.py
```

### Listar todas las cuentas:
```powershell
python listar_cuentas.py
```

---

## 💡 NOTAS

- **Login:** El sistema usa el **email** como nombre de usuario
- **Formato:** Usa el email completo, no solo el nombre de usuario
- **Estado:** Todos los usuarios están en estado "activo"
- **Autenticación:** Verificada y funcionando correctamente

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### "Credenciales inválidas"
1. Ejecuta: `python reparar_cuentas.py`
2. Verifica que uses el email completo
3. Verifica que la contraseña sea correcta (sensible a mayúsculas)

### "Usuario inactivo"
1. Ejecuta: `python reparar_cuentas.py`
2. Esto activará automáticamente todos los usuarios

### Olvidé las credenciales
Consulta este archivo o ejecuta:
```powershell
python listar_cuentas.py
```

---

**¡Todas las cuentas están funcionando correctamente!** ✅
