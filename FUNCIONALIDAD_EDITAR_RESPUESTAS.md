# 📝 NUEVA FUNCIONALIDAD: Edición de Respuestas del Profesor

**Fecha:** 01/12/2025  
**Asignación:** Según recomendación del docente

---

## 🎯 Objetivo

Permitir que los profesores puedan editar, visualizar y gestionar las respuestas que ya han enviado a las consultas de los estudiantes, brindándoles la oportunidad de corregir errores o mejorar sus explicaciones.

---

## ✨ Características Implementadas

### 1. Dashboard Docente Mejorado

**Ubicación:** `EduConnectApp/templates/EduConnectApp/dashboard_docente.html`

#### Nuevo KPI
- **Respuestas Guardadas**: Muestra el total de respuestas que ha enviado el profesor
- **Sección dedicada** con lista de todas las respuestas

#### Nueva Tabla: "Mis Respuestas Guardadas"
- Listado completo de todas las respuestas enviadas
- Información: Fecha, Estudiante, Pregunta, Asignatura, Tipo de Respuesta
- **3 acciones por cada respuesta:**
  - 👁️ **Ver**: Visualizar la respuesta en detalle
  - ✏️ **Editar**: Modificar la respuesta existente
  - 🗑️ **Eliminar**: Borrar la respuesta

---

## 🔧 Cambios en el Backend

### Vistas Nuevas (`EduConnectApp/views.py`)

#### 1. `editar_respuesta(request, respuesta_id)`
- **Ruta:** `/respuesta/<id>/editar/`
- **Permisos:** Solo docentes
- **Funcionalidad:**
  - Verifica que la respuesta pertenezca al docente logueado
  - Permite editar: contenido, tipo de respuesta, archivo adjunto
  - Actualiza el campo `updated_at` con fecha actual
  - Muestra la consulta original como referencia
  - Redirige al dashboard tras guardar

#### 2. `ver_respuesta(request, respuesta_id)`
- **Ruta:** `/respuesta/<id>/ver/`
- **Permisos:** Docente autor, admin, o estudiante propietario
- **Funcionalidad:**
  - Visualización completa de la respuesta
  - Muestra la consulta original y la respuesta con toda su información
  - Solo permite editar si eres el autor

#### 3. `eliminar_respuesta(request, respuesta_id)`
- **Ruta:** `/respuesta/<id>/eliminar/`
- **Método:** POST (tras confirmación)
- **Funcionalidad:**
  - Verifica propiedad de la respuesta
  - Elimina archivos adjuntos del servidor
  - Vuelve la consulta a estado "pendiente"
  - Muestra página de confirmación antes de eliminar

### Modelo Actualizado (`EduConnectApp/models.py`)

El modelo `Respuestas` ya incluye:
- `updated_at`: Fecha de última actualización
- `contenido_respuesta`: Campo de contenido
- `tipo_respuesta`: Tipo de respuesta (académica, orientación, administrativa, etc.)
- `adjunto_archivo`: Campo para archivos

### Formulario Actualizado (`EduConnectApp/forms.py`)

```python
class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuestas
        fields = ['contenido_respuesta', 'tipo_respuesta', 'adjunto_archivo']
        widgets = {
            'contenido_respuesta': forms.Textarea(...),
            'tipo_respuesta': forms.Select(...),
            'adjunto_archivo': forms.FileInput(...)
        }
```

### URLs Nuevas (`EduConnectApp/urls.py`)

```python
path('respuesta/<int:respuesta_id>/ver/', views.ver_respuesta, name='ver_respuesta'),
path('respuesta/<int:respuesta_id>/editar/', views.editar_respuesta, name='editar_respuesta'),
path('respuesta/<int:respuesta_id>/eliminar/', views.eliminar_respuesta, name='eliminar_respuesta'),
```

---

## 🎨 Templates Nuevos

### 1. `editar_respuesta.html`
**Ubicación:** `EduConnectApp/templates/EduConnectApp/editar_respuesta.html`

**Elementos:**
- Header con información de la acción
- Botón "Volver al Dashboard"
- **Sección izquierda (8 columnas):**
  - Card con consulta original (referencia)
  - Formulario de edición
    - Textarea para contenido
    - Select para tipo de respuesta
    - Input para archivo adjunto
  - Botones: Guardar Cambios, Cancelar

- **Sidebar derecho (4 columnas):**
  - Información de la respuesta actual
  - Fecha de respuesta original
  - Tiempo de respuesta
  - Estado de aceptación
  - Consejos para editar

### 2. `ver_respuesta.html`
**Ubicación:** `EduConnectApp/templates/EduConnectApp/ver_respuesta.html`

**Elementos:**
- Header con información de visualización
- **Sección izquierda:**
  - Card consulta original (referencia)
  - Card respuesta completa
    - Tipo de respuesta (badge)
    - Contenido formateado
    - Archivo adjunto (si existe)
    - Información de tiempos
  - Card estado de la respuesta

- **Sidebar derecho:**
  - Botones de acción (editar/eliminar si eres autor)
  - Estadísticas de evaluación
  - Información de contacto del estudiante
  - Botón volver

### 3. `confirmar_eliminar_respuesta.html`
**Ubicación:** `EduConnectApp/templates/EduConnectApp/confirmar_eliminar_respuesta.html`

**Elementos:**
- Alerta de confirmación
- Advertencia de acción irreversible
- Información de la respuesta a eliminar
- Formulario POST de confirmación
- Información de ayuda
- Botones: Confirmar eliminación, Cancelar

---

## 📊 Vista del Dashboard Mejorado

### Antes
```
┌─────────────────────────────────────────┐
│ Dashboard Docente                        │
├─────────────────────────────────────────┤
│ ┌─────────┬─────────┬──────────┐        │
│ │Pendientes│Hoy     │Asignaturas       │
│ │   15    │   3    │    4             │
│ └─────────┴─────────┴──────────┘        │
├─────────────────────────────────────────┤
│ Consultas Pendientes                     │
│ [Tabla de consultas]                     │
└─────────────────────────────────────────┘
```

### Después
```
┌─────────────────────────────────────────┐
│ Dashboard Docente                        │
├─────────────────────────────────────────┤
│ ┌─────────┬─────────┬──────────┬──────────┐
│ │Pendientes│Hoy    │Asignaturas│Respuestas│
│ │   15    │  3    │    4    │   42      │
│ └─────────┴─────────┴──────────┴──────────┘
├─────────────────────────────────────────┤
│ Consultas Pendientes                     │
│ [Tabla de consultas por responder]        │
├─────────────────────────────────────────┤
│ MIS RESPUESTAS GUARDADAS ★ NUEVO         │
│ [Tabla de respuestas enviadas]           │
│  - Fecha | Estudiante | Pregunta | ...   │
│  - 👁️ Ver | ✏️ Editar | 🗑️ Eliminar    │
└─────────────────────────────────────────┘
```

---

## 🔄 Flujo de Uso

### Editar una Respuesta

```
1. Dashboard Docente
   ↓
2. Sección "Mis Respuestas Guardadas"
   ↓
3. Click en botón "Editar" (lápiz)
   ↓
4. Página de Edición
   - Ver consulta original
   - Editar contenido, tipo, archivo
   ↓
5. Click "Guardar Cambios"
   ↓
6. Volver a Dashboard (con mensaje de éxito)
```

### Ver una Respuesta

```
1. Dashboard Docente
   ↓
2. Sección "Mis Respuestas Guardadas"
   ↓
3. Click en botón "Ver" (ojo)
   ↓
4. Página de Detalle
   - Ver consulta original
   - Ver respuesta completa
   - Ver información de tiempos
   - Opción para editar si eres autor
```

### Eliminar una Respuesta

```
1. Dashboard Docente
   ↓
2. Sección "Mis Respuestas Guardadas"
   ↓
3. Click en botón "Eliminar" (papelera)
   ↓
4. Página de Confirmación
   - Mostrar detalles de la respuesta
   - Advertencia de acción irreversible
   ↓
5. Click "Sí, Eliminar Respuesta"
   ↓
6. Volver a Dashboard (consulta ahora pendiente)
```

---

## 🔒 Controles de Seguridad

1. **Validación de Propiedad**
   - Solo el docente que envió la respuesta puede editarla
   - Se verifica el ID del docente vs el usuario en sesión

2. **CSRF Protection**
   - Todas las vistas POST tienen `@csrf_protect`
   - Los formularios incluyen token CSRF

3. **Autenticación**
   - Solo docentes pueden acceder a estas funciones
   - Verificación de sesión en todas las vistas

4. **Manejo de Archivos**
   - Los archivos se guardan en carpeta `adjuntos/`
   - Se valida el tipo MIME
   - Se elimina el archivo anterior al actualizar

---

## 📝 Cambios en la Vista dashboard_docente

**Archivo:** `EduConnectApp/views.py` (línea 350)

```python
def dashboard_docente(request):
    # ... código anterior ...
    
    # NUEVO: Respuestas guardadas por el docente
    respuestas_guardadas = Respuestas.objects.filter(
        id_docente=docente.id_docente
    ).select_related(
        'id_consulta__id_estudiante__id_usuario',
        'id_consulta__id_asignatura'
    ).order_by('-fecha_respuesta')[:20]  # Últimas 20
    
    # ... contexto ...
    context = {
        'respuestas_guardadas': respuestas_guardadas,
        'total_respuestas_guardadas': Respuestas.objects.filter(
            id_docente=docente.id_docente
        ).count(),
        # ... demás datos ...
    }
```

---

## ✅ Pruebas Realizadas

- [x] Edición de respuesta existente
- [x] Visualización de respuesta con todos los detalles
- [x] Eliminación de respuesta con confirmación
- [x] Actualización del campo `updated_at`
- [x] Validación de propiedad del docente
- [x] Redirección correcta tras cada acción
- [x] Mensaje de éxito/error al usuario
- [x] Manejo correcto de archivos adjuntos
- [x] Dashboard muestra todas las respuestas guardadas
- [x] Filtros y ordenamiento por fecha

---

## 🚀 Próximas Mejoras (Opcionales)

1. **Historial de Cambios**
   - Guardar versiones anteriores de respuestas

2. **Notificaciones**
   - Avisar al estudiante cuando se edita una respuesta

3. **Búsqueda y Filtros**
   - Filtrar respuestas por fecha, estudiante, asignatura

4. **Comentarios**
   - Permitir que estudiantes comenten sobre las respuestas

5. **Exportación**
   - Descargar historial de respuestas en PDF

6. **Analytics**
   - Estadísticas de ediciones por respuesta
   - Tiempo promedio de edición

---

## 📞 Soporte

Si necesitas ayuda con la nueva funcionalidad:
1. Verifica que estés logueado como docente
2. Accede al Dashboard Docente
3. Busca la sección "Mis Respuestas Guardadas"
4. Usa los botones de Ver, Editar o Eliminar

**Nota:** Esta funcionalidad está disponible solo para docentes y se integra completamente con el sistema existente de consultas y respuestas.

---

**Última actualización:** 01/12/2025
