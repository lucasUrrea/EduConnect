# 🏗️ ARQUITECTURA: Sistema de Edición de Respuestas

```
┌─────────────────────────────────────────────────────────────────┐
│                    NAVEGADOR DEL USUARIO                         │
│                      (Docente Logueado)                          │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────┐
    │   DASHBOARD DOCENTE          │
    │  /dashboard/docente/         │
    └────────────┬────────────────┘
                 │
        ┌────────┴────────┬──────────────┬──────────────┐
        │                 │              │              │
        ▼                 ▼              ▼              ▼
    ┌───────────┐   ┌─────────────┐ ┌────────────┐ ┌─────────┐
    │   VER     │   │   EDITAR    │ │  ELIMINAR  │ │ DETALLE │
    │ (👁️ botón)│   │  (✏️ botón) │ │ (🗑️ botón)│ │ Consulta│
    └─────┬─────┘   └──────┬──────┘ └─────┬──────┘ └────┬────┘
          │                │              │             │
          ▼                ▼              ▼             ▼
    ┌─────────────┐ ┌────────────────┐ ┌──────────────┐ ┌──────────┐
    │  GET /resp  │ │ GET /resp/edit │ │ GET /resp/rm │ │ Consulta │
    │  /id/ver/   │ │    /id/editar/ │ │ /id/eliminar/│ │ Original │
    │             │ │                │ │              │ │          │
    │ (Vista)     │ │ (Formulario)   │ │(Confirmación)│ │(Info Ref)│
    └─────┬─────┘ └────────┬────────┘ └────────┬─────┘ └──────────┘
          │                │                   │
          │                ▼                   │
          │          ┌──────────────┐          │
          │          │ form_edicion │          │
          │          │ - contenido  │          │
          │          │ - tipo       │          │
          │          │ - archivo    │          │
          │          └────────┬─────┘          │
          │                   │                │
          │                   ▼                │
          │          ┌──────────────┐          │
          │          │ POST /resp/  │          │
          │          │   id/editar/ │          │
          │          └────────┬─────┘          │
          │                   │                │
          ├───────────────────┼────────────────┤
          │                   │                │
          ▼                   ▼                ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ Template de  │ │ Actualizar   │ │ Eliminar &   │
    │ Visualización│ │ en BD        │ │ Volver a     │
    │              │ │ (updated_at) │ │ "pendiente"  │
    └──────────────┘ └────────┬─────┘ └──────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │ Redirigir a      │
                    │ Dashboard        │
                    │ (con mensaje)    │
                    └──────────────────┘
```

---

## 📦 ESTRUCTURA DE ARCHIVOS MODIFICADOS

```
EduConnectApp/
│
├── views.py
│   ├── dashboard_docente()           ⭐ MODIFICADO
│   │   ├── Obtiene respuestas_guardadas
│   │   └── Contexto con nuevas variables
│   │
│   ├── editar_respuesta()            ✨ NUEVO
│   │   ├── GET: Muestra formulario
│   │   └── POST: Guarda cambios
│   │
│   ├── ver_respuesta()               ✨ NUEVO
│   │   ├── Visualiza detalles
│   │   └── Muestra referencia
│   │
│   └── eliminar_respuesta()          ✨ NUEVO
│       ├── GET: Confirmación
│       └── POST: Ejecuta eliminación
│
├── urls.py                           ⭐ MODIFICADO
│   ├── path('respuesta/.../ver/...')
│   ├── path('respuesta/.../editar/...')
│   └── path('respuesta/.../eliminar/...')
│
├── forms.py                          ⭐ MODIFICADO
│   └── RespuestaForm
│       ├── contenido_respuesta (TextArea)
│       ├── tipo_respuesta (Select)
│       └── adjunto_archivo (FileInput)
│
├── models.py                         ✓ SIN CAMBIOS
│   └── Modelo Respuestas: campos ya existen
│
└── templates/
    ├── dashboard_docente.html        ⭐ MODIFICADO
    │   └── Nueva sección de respuestas
    │
    ├── editar_respuesta.html         ✨ NUEVO
    │   ├── Header
    │   ├── Consulta referencia
    │   ├── Formulario
    │   └── Sidebar info
    │
    ├── ver_respuesta.html            ✨ NUEVO
    │   ├── Header
    │   ├── Consulta referencia
    │   ├── Respuesta completa
    │   ├── Estado
    │   └── Sidebar acciones
    │
    └── confirmar_eliminar_respuesta.html ✨ NUEVO
        ├── Alerta
        ├── Detalles
        ├── Confirmación
        └── Ayuda
```

---

## 🔄 FLUJO DE EDICIÓN EN DETALLE

```
┌─────────────────────────────────────────────────────────────┐
│ 1. USUARIO EN DASHBOARD                                      │
├─────────────────────────────────────────────────────────────┤
│   Dashboard Docente (/dashboard/docente/)                   │
│   ├─ Consultas Pendientes (lista)                           │
│   └─ Mis Respuestas Guardadas ⭐ NUEVA SECCIÓN             │
│      └─ Tabla con respuestas                               │
│         ├─ Col: Fecha, Estudiante, Pregunta, etc          │
│         └─ Acciones: Ver | Editar | Eliminar              │
└─────────────────────────────────────────────────────────────┘
                        │
                        │ Click en ✏️ Editar
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. FORMULARIO DE EDICIÓN                                     │
├─────────────────────────────────────────────────────────────┤
│   GET /respuesta/<id>/editar/                              │
│   ├─ Validación: ¿Es tu respuesta? ✓                      │
│   └─ Renderizar template: editar_respuesta.html            │
│
│   Contenido mostrado:                                       │
│   ├─ IZQUIERDA (8 cols)                                    │
│   │  ├─ Card: Consulta Original (referencia)              │
│   │  │  ├─ Estudiante: Juan Pérez                         │
│   │  │  ├─ Asignatura: Cálculo                            │
│   │  │  ├─ Pregunta: "¿Cómo derivar...?"                 │
│   │  │  └─ Prioridad: Alta                                │
│   │  │
│   │  └─ Card: Formulario de Edición                       │
│   │     ├─ Textarea: contenido_respuesta (10 líneas)     │
│   │     ├─ Select: tipo_respuesta                         │
│   │     │  ├─ académica                                   │
│   │     │  ├─ orientación                                 │
│   │     │  └─ administrativa                              │
│   │     ├─ FileInput: adjunto_archivo                     │
│   │     └─ Botones: [Guardar Cambios] [Cancelar]         │
│   │
│   └─ DERECHA (4 cols)                                     │
│      ├─ Info: Fecha original, Tipo, Estado               │
│      ├─ Consejos para editar                              │
│      └─ Validaciones activas                              │
└─────────────────────────────────────────────────────────────┘
                        │
                        │ Submit del formulario
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. PROCESAMIENTO EN BACKEND                                 │
├─────────────────────────────────────────────────────────────┤
│   POST /respuesta/<id>/editar/                             │
│
│   1. Validación CSRF
│   2. Obtener respuesta de BD
│   3. Verificar propiedad
│   4. Validar formulario (RespuestaForm)
│   5. Si válido:
│   │  ├─ Actualizar contenido_respuesta
│   │  ├─ Actualizar tipo_respuesta
│   │  ├─ Guardar nuevo archivo (si existe)
│   │  ├─ Establecer updated_at = ahora()
│   │  ├─ Guardar en BD
│   │  ├─ messages.success()
│   │  └─ Redirigir a dashboard_docente
│   │
│   6. Si inválido:
│      ├─ messages.error()
│      └─ Re-renderizar con errores
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. VUELTA AL DASHBOARD                                      │
├─────────────────────────────────────────────────────────────┤
│   GET /dashboard/docente/                                  │
│   ├─ Mensaje: "✓ Respuesta actualizada correctamente"   │
│   └─ Tabla actualizada con:                              │
│      └─ Fecha anterior pero updated_at nuevo             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔒 CAPAS DE SEGURIDAD

```
REQUEST
│
├─ ✅ CSRF Token presente
│
├─ ✅ Session válida
│   └─ usuario_id en sesión
│
├─ ✅ Tipo de usuario correcto
│   └─ tipo_usuario == 'docente'
│
├─ ✅ Recurso existe
│   └─ Respuesta con id_respuesta
│
├─ ✅ Propiedad verificada
│   └─ respuesta.id_docente == usuario_logueado
│
├─ ✅ Validación de formulario
│   └─ RespuestaForm valida campos
│
├─ ✅ Manejo de archivos seguro
│   └─ default_storage.save()
│
└─ ✅ Logging de cambios
    └─ logger.info() / logger.exception()
```

---

## 📊 TABLA DE RESPUESTAS EN DASHBOARD

```
┌─────┬──────────┬──────────┬──────────┬──────────┬──────────┬─────────┐
│Fecha│Estudiante│ Pregunta │Asignatura│   Tipo   │Respuestas│Acciones │
├─────┼──────────┼──────────┼──────────┼──────────┼──────────┼─────────┤
│30/11│JP        │Derivadas │MAT-101   │Académica │01/12     │👁️✏️🗑️ │
│29/11│MC        │Integrales│MAT-102   │Académica │01/12     │👁️✏️🗑️ │
│28/11│AB        │Límites   │MAT-101   │Orient.   │01/12     │👁️✏️🗑️ │
│27/11│DF        │Matrices  │ALG-201   │Académica │01/12     │👁️✏️🗑️ │
└─────┴──────────┴──────────┴──────────┴──────────┴──────────┴─────────┘

👁️ = Ver   ✏️ = Editar   🗑️ = Eliminar
```

---

## 🎯 PUNTOS CLAVE DE LA IMPLEMENTACIÓN

### 1. Dashboard Mejorado
- ✅ Nuevo KPI: "Respuestas Guardadas"
- ✅ Nueva tabla con historial completo
- ✅ 3 acciones rápidas por respuesta

### 2. Edición Funcional
- ✅ Formulario pre-llenado con datos actuales
- ✅ Referencia a consulta original
- ✅ Manejo de archivos adjuntos
- ✅ Actualización de timestamp

### 3. Visualización Detallada
- ✅ Vista completa con información
- ✅ Referencia a consulta original
- ✅ Detalles de tiempos y estado
- ✅ Botón para editar (si eres autor)

### 4. Eliminación Segura
- ✅ Confirmación antes de eliminar
- ✅ Detalles de lo que se elimina
- ✅ Limpieza de archivos servidor
- ✅ Vuelve consulta a "pendiente"

### 5. Seguridad
- ✅ CSRF Protection en formularios
- ✅ Validación de propiedad
- ✅ Verificación de sesión
- ✅ Control de permisos por rol

---

## 🚀 USO RÁPIDO

```
1. Acceder como Docente
   └─ /login/  →  Credenciales

2. Dashboard
   └─ /dashboard/docente/

3. Scroll hasta "Mis Respuestas Guardadas"
   └─ Nueva tabla ⭐

4. Seleccionar Acción
   ├─ Ver    (👁️)  → Detalle
   ├─ Editar (✏️)  → Formulario
   └─ Eliminar (🗑️) → Confirmación

5. Listo
   └─ Todas las acciones guardan cambios
```

---

## 📋 CHECKLIST DE FUNCIONALIDADES

- [x] Dashboard muestra respuestas guardadas
- [x] Nueva tabla con información completa
- [x] Botón Ver funciona correctamente
- [x] Botón Editar abre formulario
- [x] Formulario guarda cambios
- [x] Campo updated_at se actualiza
- [x] Validación de propiedad
- [x] Manejo de archivos adjuntos
- [x] Botón Eliminar pide confirmación
- [x] Eliminación limpia archivos
- [x] CSRF protection en todos los forms
- [x] Mensajes de éxito/error
- [x] Redirecciones correctas
- [x] Estilos consistentes

---

**Documentación de arquitectura: 01/12/2025**
