from django.contrib import admin
from .models import *

# Register models to appear in Django admin
@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
	list_display = ('id_usuario', 'email', 'tipo_usuario', 'estado')
	search_fields = ('email', 'nombre', 'apellido_paterno')


@admin.register(Consultas)
class ConsultasAdmin(admin.ModelAdmin):
	list_display = ('id_consulta', 'titulo', 'id_asignatura', 'id_estudiante', 'estado', 'fecha_consulta')
	search_fields = ('titulo', 'descripcion')
	list_filter = ('estado', 'prioridad')


@admin.register(Respuestas)
class RespuestasAdmin(admin.ModelAdmin):
	list_display = ('id_respuesta', 'id_consulta', 'id_docente', 'fecha_respuesta')
	search_fields = ('contenido_respuesta',)
# Improved admin: allow editing which courses a docente teaches inline on the Docentes admin
class DocenteAsignaturaInline(admin.TabularInline):
	model = DocenteAsignatura
	extra = 1
	verbose_name = 'Asignatura impartida'
	verbose_name_plural = 'Asignaturas impartidas'


@admin.register(Docentes)
class DocentesAdmin(admin.ModelAdmin):
	list_display = ('id_docente', 'id_usuario', 'codigo_docente', 'departamento')
	search_fields = ('codigo_docente', 'id_usuario__email')
	inlines = [DocenteAsignaturaInline]


@admin.register(Asignaturas)
class AsignaturasAdmin(admin.ModelAdmin):
	list_display = ('id_asignatura', 'codigo_asignatura', 'nombre_asignatura', 'estado')
	search_fields = ('codigo_asignatura', 'nombre_asignatura')


admin.site.register(Estudiantes)
admin.site.register(CategoriasTemas)
admin.site.register(ArchivosAdjuntos)
admin.site.register(Notificaciones)
admin.site.register(LogsActividad)
admin.site.register(DocenteAsignatura)
# Register your models here.
