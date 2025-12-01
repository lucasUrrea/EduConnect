# 🗂️ REFERENCIA RÁPIDA: Nueva Funcionalidad de Edición de Respuestas

---

## 📍 UBICACIÓN DE COMPONENTES

### 🔧 Backend (Python)

#### Vistas
```python
# Archivo: EduConnectApp/views.py

dashboard_docente(request)              # Línea ~350 - MODIFICADO
  ✅ Agrega respuestas_guardadas
  ✅ Agrega total_respuestas_guardadas

editar_respuesta(request, respuesta_id) # Línea ~560 - NUEVO
  ✅ Formulario de edición
  ✅ Validación de propiedad
  ✅ Actualiza updated_at

ver_respuesta(request, respuesta_id)    # Línea ~605 - NUEVO
  ✅ Visualización completa
  ✅ Información detallada

eliminar_respuesta(request, respuesta_id) # Línea ~640 - NUEVO
  ✅ Confirmación de eliminación
  ✅ Elimina archivos
  ✅ Vuelve consulta a "pendiente"
```

#### URLs
```python
# Archivo: EduConnectApp/urls.py (Línea ~19)

path('respuesta/<int:respuesta_id>/ver/', views.ver_respuesta, name='ver_respuesta'),
path('respuesta/<int:respuesta_id>/editar/', views.editar_respuesta, name='editar_respuesta'),
path('respuesta/<int:respuesta_id>/eliminar/', views.eliminar_respuesta, name='eliminar_respuesta'),
```

#### Formularios
```python
# Archivo: EduConnectApp/forms.py (Línea ~19)

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuestas
        fields = ['contenido_respuesta', 'tipo_respuesta', 'adjunto_archivo']
        # Con widgets personalizados
```

---

### 🎨 Frontend (Templates HTML)

#### Dashboard Docente
```html
<!-- Archivo: EduConnectApp/templates/EduConnectApp/dashboard_docente.html -->

<!-- KPI Nuevo (Línea ~50) -->
<div class="col-xl-3 col-md-6">
    <div class="kpi-card kpi-purple">
        <div class="kpi-value">{{ total_respuestas_guardadas }}</div>
        <div class="kpi-label">Respuestas Guardadas</div>
    </div>
</div>

<!-- Tabla de Respuestas (Línea ~310) -->
<div class="section-card">
    <div class="section-header">
        <h5><i class="fas fa-save me-2"></i>Mis Respuestas Guardadas</h5>
    </div>
    <table class="table table-hover">
        <!-- Columnas: Fecha, Estudiante, Pregunta, Asignatura, Tipo, Acciones -->
        <!-- Botones: Ver, Editar, Eliminar -->
    </table>
</div>

<!-- JavaScript (Línea ~580) -->
<script>
function confirmarEliminacion(respuestaId) { ... }
</script>
```

#### Editar Respuesta - NUEVO
```html
<!-- Archivo: EduConnectApp/templates/EduConnectApp/editar_respuesta.html -->

<!-- Header -->
<h2><i class="fas fa-edit text-warning me-2"></i>Editar Respuesta</h2>

<!-- Main (8 columnas) -->
<div class="col-lg-8">
    <!-- Consulta Original -->
    <div class="card" style="border-left: 4px solid #3b82f6;">
        <!-- Información de referencia de la consulta -->
    </div>
    
    <!-- Formulario -->
    <div class="card">
        <!-- Textarea: contenido_respuesta -->
        <!-- Select: tipo_respuesta -->
        <!-- FileInput: adjunto_archivo -->
        <!-- Botones: Guardar, Cancelar -->
    </div>
</div>

<!-- Sidebar (4 columnas) -->
<div class="col-lg-4">
    <!-- Información de la respuesta -->
    <!-- Consejos para editar -->
</div>
```

#### Ver Respuesta - NUEVO
```html
<!-- Archivo: EduConnectApp/templates/EduConnectApp/ver_respuesta.html -->

<!-- Header -->
<h2><i class="fas fa-reply text-success me-2"></i>Detalle de Respuesta</h2>

<!-- Main (8 columnas) -->
<div class="col-lg-8">
    <!-- Consulta Original -->
    <div class="card" style="border-left: 4px solid #3b82f6;">
        <!-- Información de la consulta -->
    </div>
    
    <!-- Respuesta -->
    <div class="card" style="border-left: 4px solid #10b981;">
        <!-- Tipo, Contenido, Archivo, Tiempos -->
    </div>
    
    <!-- Estado -->
    <div class="card">
        <!-- Estado de la respuesta -->
    </div>
</div>

<!-- Sidebar (4 columnas) -->
<div class="col-lg-4">
    <!-- Botones de acción -->
    <!-- Estadísticas de evaluación -->
    <!-- Información de contacto -->
</div>
```

#### Confirmar Eliminar - NUEVO
```html
<!-- Archivo: EduConnectApp/templates/EduConnectApp/confirmar_eliminar_respuesta.html -->

<!-- Alerta de confirmación -->
<div class="card border-danger">
    <!-- Advertencia -->
    <!-- Información de lo que se eliminará -->
    <!-- Formulario POST con CSRF -->
    <!-- Información de ayuda -->
</div>
```

---

## 🔄 Flujo de Datos

```
Dashboard Docente
├── GET /dashboard/docente/
├── Obtiene respuestas_guardadas de BD
└── Muestra tabla con respuestas

│
├── EDITAR
│   ├── Click en botón Editar (ícono lápiz)
│   ├── GET /respuesta/<id>/editar/
│   ├── Muestra formulario con datos
│   └── POST /respuesta/<id>/editar/
│       ├── Valida propiedad
│       ├── Actualiza campos
│       ├── Guarda en BD
│       └── Redirige a dashboard

├── VER
│   ├── Click en botón Ver (ícono ojo)
│   └── GET /respuesta/<id>/ver/
│       └── Muestra respuesta con todos detalles

└── ELIMINAR
    ├── Click en botón Eliminar (ícono papelera)
    ├── GET /respuesta/<id>/eliminar/
    ├── Muestra confirmación
    └── POST /respuesta/<id>/eliminar/
        ├── Valida propiedad
        ├── Elimina archivo adjunto
        ├── Elimina respuesta de BD
        ├── Vuelve consulta a "pendiente"
        └── Redirige a dashboard
```

---

## 🎯 ACCESOS RÁPIDOS

### Ver Nueva Funcionalidad
1. **Dashboard Docente**: `/dashboard/docente/`
2. **Scroll hacia abajo**: Busca "Mis Respuestas Guardadas"
3. **Tabla con 3 botones**: Ver | Editar | Eliminar

### Editar una Respuesta
- **URL**: `/respuesta/<id>/editar/`
- **Método**: GET (mostrar form) / POST (guardar)
- **Auth**: Solo docente autor
- **Redirige a**: `/dashboard/docente/`

### Ver Detalle
- **URL**: `/respuesta/<id>/ver/`
- **Método**: GET
- **Auth**: Docente autor, admin, o estudiante propietario

### Eliminar
- **URL**: `/respuesta/<id>/eliminar/`
- **Confirmación**: GET (mostrar formulario) / POST (ejecutar)
- **Auth**: Solo docente autor

---

## 📊 Variables en Templates

### En Dashboard Docente
```django
{{ total_respuestas_guardadas }}    # Total de respuestas
{{ respuestas_guardadas }}          # List de respuestas (últimas 20)

<!-- Cada respuesta contiene: -->
respuesta.id_respuesta              # ID para URLs
respuesta.id_consulta               # Referencia a consulta
respuesta.fecha_respuesta           # Fecha de envío
respuesta.tipo_respuesta            # Tipo: académica, orientación, etc
respuesta.es_aceptada               # Si fue aceptada por estudiante
respuesta.id_docente                # Referencia al docente (verificación)
respuesta.id_consulta.id_estudiante # Estudiante que consultó
respuesta.id_consulta.id_asignatura # Asignatura de la consulta
```

### En Templates de Respuesta
```django
respuesta.contenido_respuesta       # Contenido de la respuesta
respuesta.adjunto_archivo           # Archivo adjunto
respuesta.tiempo_respuesta_horas    # Horas para responder
respuesta.updated_at                # Fecha última actualización
respuesta.es_respuesta_definitiva   # Si es definitiva
respuesta.calificacion_respuesta    # JSON de calificaciones

consulta.titulo                     # Título de la pregunta
consulta.descripcion                # Descripción completa
consulta.prioridad                  # Nivel: baja, media, alta, urgente
consulta.fecha_consulta             # Fecha de la consulta
```

---

## 🔐 Validaciones Implementadas

```python
# Propiedad de respuesta
if respuesta.id_docente.id_docente != docente.id_docente:
    # No es propietario: acceso denegado

# Rol correcto
if request.session.get('tipo_usuario') != 'docente':
    # No es docente: redirige a login

# Sesión activa
if 'usuario_id' not in request.session:
    # Sin sesión: redirige a login
```

---

## 💾 Campos BD Utilizados

```sql
-- Tabla: respuestas
respuesta.id_respuesta              -- PK Auto
respuesta.contenido_respuesta       -- TextField (modificable)
respuesta.tipo_respuesta            -- CharField (modificable)
respuesta.adjunto_archivo           -- FileField (modificable)
respuesta.fecha_respuesta           -- DateTime (solo lectura)
respuesta.updated_at                -- DateTime (auto actualizado)
respuesta.id_docente                -- FK (verificación)
respuesta.id_consulta               -- FK (referencia)
respuesta.tiempo_respuesta_horas    -- Int (calculado)
respuesta.es_aceptada               -- Int (no modificable)
```

---

## 🎨 Estilos CSS Incluidos

```css
/* En los templates */
.section-card              /* Card principal */
.section-header            /* Header de sección */
.table-responsive          /* Tabla responsiva */
.badge bg-info/warning/etc /* Estados con color */
.student-avatar            /* Avatar del estudiante */
.alert alert-info/danger   /* Alertas */
.btn btn-warning/info      /* Botones */
```

---

## 🚀 PARA USAR INMEDIATAMENTE

1. **Accede como docente** a tu cuenta
2. **Ve a Dashboard** → `/dashboard/docente/`
3. **Scroll** hasta "Mis Respuestas Guardadas"
4. **Elige acción**: Ver | Editar | Eliminar
5. **Listo** - ¡A usar!

---

## 📝 NOTAS IMPORTANTES

- ✅ No requiere migraciones de BD
- ✅ Compatible con SQLite y MySQL
- ✅ Usa campos existentes del modelo
- ✅ Mantiene seguridad del proyecto
- ✅ Integrado con sistema de permisos
- ✅ Respeta validaciones CSRF

---

**Creado:** 01/12/2025
