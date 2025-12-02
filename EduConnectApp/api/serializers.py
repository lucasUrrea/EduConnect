from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from ..models import (
    Consultas, Respuestas, Usuarios, Asignaturas, CategoriasTemas, 
    Docentes, Estudiantes, DocenteAsignatura, Notificaciones, 
    EvaluacionesRespuesta, LogsActividad, Seguimientos
)


# ==============================================================================
# USUARIOS SERIALIZERS
# ==============================================================================
class UsuariosSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Usuarios - Solo información pública.
    NUNCA expone password_hash ni información sensible.
    """
    nombre_completo = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Usuarios
        fields = [
            'id_usuario', 'email', 'tipo_usuario', 'nombre', 
            'apellido_paterno', 'apellido_materno', 'telefono',
            'foto_perfil', 'estado', 'nombre_completo'
        ]
        read_only_fields = [
            'id_usuario', 'fecha_registro', 'ultimo_acceso', 
            'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'tipo_usuario': {'required': True},
            'nombre': {'required': True},
            'apellido_paterno': {'required': True},
        }
    
    def get_nombre_completo(self, obj):
        """Retorna el nombre completo del usuario"""
        partes = [obj.nombre, obj.apellido_paterno]
        if obj.apellido_materno:
            partes.append(obj.apellido_materno)
        return ' '.join(partes)
    
    def validate_email(self, value):
        """Valida que el email sea único y válido"""
        if value and not '@' in value:
            raise serializers.ValidationError("Email inválido")
        return value.lower()
    
    def validate_tipo_usuario(self, value):
        """Valida que el tipo de usuario sea válido"""
        tipos_validos = ['estudiante', 'docente', 'admin']
        if value not in tipos_validos:
            raise serializers.ValidationError(
                f"Tipo de usuario inválido. Debe ser uno de: {', '.join(tipos_validos)}"
            )
        return value


class UsuariosDetailSerializer(UsuariosSerializer):
    """Serializer extendido con más detalles para vistas autenticadas"""
    
    class Meta(UsuariosSerializer.Meta):
        fields = UsuariosSerializer.Meta.fields + [
            'fecha_registro', 'ultimo_acceso', 'created_at'
        ]


# ==============================================================================
# ESTUDIANTES SERIALIZERS
# ==============================================================================
class EstudiantesSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Estudiantes"""
    usuario = UsuariosSerializer(source='id_usuario', read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuarios.objects.all(),
        source='id_usuario',
        write_only=True
    )
    
    class Meta:
        model = Estudiantes
        fields = [
            'id_estudiante', 'usuario', 'usuario_id', 'numero_matricula',
            'carrera', 'semestre', 'fecha_ingreso', 'promedio_general'
        ]
        read_only_fields = ['id_estudiante', 'created_at', 'updated_at']
        extra_kwargs = {
            'numero_matricula': {'required': True},
        }
    
    def validate_semestre(self, value):
        """Valida que el semestre sea válido"""
        if value and (value < 1 or value > 12):
            raise serializers.ValidationError("El semestre debe estar entre 1 y 12")
        return value
    
    def validate_promedio_general(self, value):
        """Valida que el promedio sea válido"""
        if value and (value < 0 or value > 10):
            raise serializers.ValidationError("El promedio debe estar entre 0 y 10")
        return value


# ==============================================================================
# DOCENTES SERIALIZERS
# ==============================================================================
class DocentesSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Docentes"""
    usuario = UsuariosSerializer(source='id_usuario', read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuarios.objects.all(),
        source='id_usuario',
        write_only=True
    )
    
    class Meta:
        model = Docentes
        fields = [
            'id_docente', 'usuario', 'usuario_id', 'codigo_docente',
            'departamento', 'titulo_academico', 'especialidades',
            'biografia', 'horario_atencion', 'tiempo_respuesta_maximo'
        ]
        read_only_fields = ['id_docente', 'created_at', 'updated_at']
        extra_kwargs = {
            'codigo_docente': {'required': True},
        }


class DocenteAsignaturaSerializer(serializers.ModelSerializer):
    """Serializer para relación Docente-Asignatura"""
    docente = DocentesSerializer(source='id_docente', read_only=True)
    asignatura = serializers.StringRelatedField(source='id_asignatura', read_only=True)
    
    class Meta:
        model = DocenteAsignatura
        fields = '__all__'
        read_only_fields = ['id_docente_asignatura', 'created_at']


# ==============================================================================
# ASIGNATURAS Y CATEGORIAS SERIALIZERS
# ==============================================================================
class AsignaturasSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Asignaturas"""
    
    class Meta:
        model = Asignaturas
        fields = [
            'id_asignatura', 'codigo_asignatura', 'nombre_asignatura',
            'descripcion', 'estado'
        ]
        read_only_fields = ['id_asignatura', 'created_at', 'updated_at']
        extra_kwargs = {
            'codigo_asignatura': {'required': True},
            'nombre_asignatura': {'required': True},
        }


class CategoriasSerializer(serializers.ModelSerializer):
    """Serializer para el modelo CategoriasTemas"""
    
    class Meta:
        model = CategoriasTemas
        fields = [
            'id_categoria', 'id_asignatura', 'nombre_categoria', 'descripcion',
            'icono', 'color_hex', 'orden_visualizacion', 'estado'
        ]
        read_only_fields = ['id_categoria', 'created_at', 'updated_at']
        extra_kwargs = {
            'nombre_categoria': {'required': True},
        }


# ==============================================================================
# CONSULTAS SERIALIZERS
# ==============================================================================
class ConsultasListSerializer(serializers.ModelSerializer):
    """Serializer ligero para listado de consultas"""
    estudiante = EstudiantesSerializer(source='id_estudiante', read_only=True)
    asignatura = AsignaturasSerializer(source='id_asignatura', read_only=True)
    categoria = CategoriasSerializer(source='id_categoria', read_only=True)
    tiempo_transcurrido = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Consultas
        fields = [
            'id_consulta', 'titulo', 'estado', 'prioridad',
            'fecha_consulta', 'tipo_consulta',
            'estudiante', 'asignatura', 'categoria', 'tiempo_transcurrido'
        ]
        read_only_fields = ['id_consulta', 'fecha_consulta']
    
    def get_tiempo_transcurrido(self, obj):
        """Calcula el tiempo transcurrido desde la consulta"""
        if obj.fecha_consulta:
            delta = timezone.now() - obj.fecha_consulta
            if delta.days > 0:
                return f"{delta.days} día(s)"
            elif delta.seconds >= 3600:
                return f"{delta.seconds // 3600} hora(s)"
            else:
                return f"{delta.seconds // 60} minuto(s)"
        return None


class ConsultasSerializer(serializers.ModelSerializer):
    """Serializer completo para consultas"""
    estudiante = EstudiantesSerializer(source='id_estudiante', read_only=True)
    asignatura = AsignaturasSerializer(source='id_asignatura', read_only=True)
    categoria = CategoriasSerializer(source='id_categoria', read_only=True)
    
    # Write-only fields para creación/actualización
    estudiante_id = serializers.PrimaryKeyRelatedField(
        queryset=Estudiantes.objects.all(),
        source='id_estudiante',
        write_only=True
    )
    asignatura_id = serializers.PrimaryKeyRelatedField(
        queryset=Asignaturas.objects.all(),
        source='id_asignatura',
        write_only=True
    )
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=CategoriasTemas.objects.all(),
        source='id_categoria',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Consultas
        fields = [
            'id_consulta', 'titulo', 'descripcion', 'prioridad', 'estado',
            'fecha_consulta', 'fecha_limite_respuesta',
            'adjunto_archivo', 'tipo_consulta', 'tags', 'es_anonima',
            'estudiante', 'asignatura', 'categoria',
            'estudiante_id', 'asignatura_id', 'categoria_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id_consulta', 'fecha_consulta', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'titulo': {'required': True, 'max_length': 200},
            'descripcion': {'required': True},
        }
    
    def validate_prioridad(self, value):
        """Valida que la prioridad sea válida"""
        prioridades_validas = ['alta', 'media', 'baja', 'urgente']
        if value and value not in prioridades_validas:
            raise serializers.ValidationError(
                f"Prioridad inválida. Debe ser una de: {', '.join(prioridades_validas)}"
            )
        return value
    
    def validate_estado(self, value):
        """Valida que el estado sea válido"""
        estados_validos = ['pendiente', 'en_proceso', 'resuelta', 'cerrada', 'cancelada']
        if value and value not in estados_validos:
            raise serializers.ValidationError(
                f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}"
            )
        return value


# ==============================================================================
# RESPUESTAS SERIALIZERS
# ==============================================================================
class RespuestasListSerializer(serializers.ModelSerializer):
    """Serializer ligero para listado de respuestas"""
    docente = DocentesSerializer(source='id_docente', read_only=True)
    
    class Meta:
        model = Respuestas
        fields = [
            'id_respuesta', 'contenido_respuesta', 'tipo_respuesta',
            'fecha_respuesta', 'es_respuesta_definitiva', 'docente'
        ]
        read_only_fields = ['id_respuesta', 'fecha_respuesta']


class RespuestasSerializer(serializers.ModelSerializer):
    """Serializer completo para respuestas"""
    consulta = ConsultasListSerializer(source='id_consulta', read_only=True)
    docente = DocentesSerializer(source='id_docente', read_only=True)
    
    consulta_id = serializers.PrimaryKeyRelatedField(
        queryset=Consultas.objects.all(),
        source='id_consulta',
        write_only=True
    )
    docente_id = serializers.PrimaryKeyRelatedField(
        queryset=Docentes.objects.all(),
        source='id_docente',
        write_only=True
    )
    
    class Meta:
        model = Respuestas
        fields = [
            'id_respuesta', 'contenido_respuesta', 'tipo_respuesta',
            'adjunto_archivo', 'fecha_respuesta', 'tiempo_respuesta_horas',
            'calificacion_respuesta', 'es_respuesta_definitiva',
            'consulta', 'docente', 'consulta_id', 'docente_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id_respuesta', 'fecha_respuesta', 'tiempo_respuesta_horas',
            'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'contenido_respuesta': {'required': True},
        }
    
    def validate_tipo_respuesta(self, value):
        """Valida que el tipo de respuesta sea válido"""
        tipos_validos = ['respuesta_directa', 'aclaracion', 'seguimiento', 'solucion']
        if value and value not in tipos_validos:
            raise serializers.ValidationError(
                f"Tipo de respuesta inválido. Debe ser uno de: {', '.join(tipos_validos)}"
            )
        return value


# ==============================================================================
# NOTIFICACIONES SERIALIZERS
# ==============================================================================
class NotificacionesSerializer(serializers.ModelSerializer):
    """Serializer para notificaciones"""
    usuario_destinatario = UsuariosSerializer(source='id_usuario_destinatario', read_only=True)
    
    class Meta:
        model = Notificaciones
        fields = [
            'id_notificacion', 'usuario_destinatario', 'tipo_notificacion',
            'titulo', 'mensaje', 'id_referencia', 'tipo_referencia',
            'leida', 'enviada_email', 'fecha_creacion', 'fecha_leida'
        ]
        read_only_fields = [
            'id_notificacion', 'fecha_creacion', 'fecha_leida'
        ]


# ==============================================================================
# EVALUACIONES SERIALIZERS
# ==============================================================================
class EvaluacionesRespuestaSerializer(serializers.ModelSerializer):
    """Serializer para evaluaciones de respuestas"""
    respuesta = RespuestasListSerializer(source='id_respuesta', read_only=True)
    estudiante = EstudiantesSerializer(source='id_estudiante', read_only=True)
    
    class Meta:
        model = EvaluacionesRespuesta
        fields = [
            'id_evaluacion', 'respuesta', 'estudiante', 'calificacion',
            'comentario_evaluacion', 'fue_util', 'resolvio_duda',
            'fecha_evaluacion'
        ]
        read_only_fields = ['id_evaluacion', 'fecha_evaluacion', 'created_at']
    
    def validate_calificacion(self, value):
        """Valida que la calificación tenga el formato correcto"""
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("La calificación debe ser un objeto JSON")
        return value


# ==============================================================================
# SEGUIMIENTOS SERIALIZERS
# ==============================================================================
class SeguimientosSerializer(serializers.ModelSerializer):
    """Serializer para seguimientos de consultas"""
    usuario = UsuariosSerializer(source='id_usuario', read_only=True)
    
    class Meta:
        model = Seguimientos
        fields = [
            'id_seguimiento', 'id_consulta', 'usuario', 'tipo_usuario',
            'mensaje', 'adjunto_archivo', 'fecha_seguimiento'
        ]
        read_only_fields = ['id_seguimiento', 'fecha_seguimiento', 'created_at']


# ==============================================================================
# LOGS SERIALIZERS
# ==============================================================================
class LogsActividadSerializer(serializers.ModelSerializer):
    """Serializer para logs de actividad - Solo lectura"""
    usuario = UsuariosSerializer(source='id_usuario', read_only=True)
    
    class Meta:
        model = LogsActividad
        fields = [
            'id_log', 'usuario', 'tipo_evento', 'descripcion',
            'ip_address', 'user_agent', 'datos_adicionales', 'fecha_evento'
        ]
        read_only_fields = '__all__'  # Los logs son solo lectura
