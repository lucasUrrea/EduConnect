from django.db import models

class ArchivosAdjuntos(models.Model):
    id_archivo = models.AutoField(primary_key=True)
    nombre_archivo = models.CharField(max_length=255)
    nombre_original = models.CharField(max_length=255)
    ruta_archivo = models.CharField(max_length=500)
    tipo_mime = models.CharField(max_length=100, blank=True, null=True)
    tamaño_bytes = models.BigIntegerField(blank=True, null=True)
    id_usuario_subida = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario_subida')
    tipo_referencia = models.CharField(max_length=11)
    id_referencia = models.IntegerField()
    fecha_subida = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'archivos_adjuntos'


class Asignaturas(models.Model):
    id_asignatura = models.AutoField(primary_key=True)
    codigo_asignatura = models.CharField(unique=True, max_length=20)
    nombre_asignatura = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    creditos = models.IntegerField(blank=True, null=True)
    semestre_recomendado = models.IntegerField(blank=True, null=True)
    carrera = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=8, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'asignaturas'


class CategoriasTemas(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    id_asignatura = models.ForeignKey(Asignaturas, models.DO_NOTHING, db_column='id_asignatura')
    nombre_categoria = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    color_hex = models.CharField(max_length=7, blank=True, null=True)
    icono = models.CharField(max_length=50, blank=True, null=True)
    orden_visualizacion = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=8, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'categorias_temas'


class ConfiguracionesSistema(models.Model):
    id_config = models.AutoField(primary_key=True)
    clave_config = models.CharField(unique=True, max_length=100)
    valor_config = models.TextField()
    descripcion = models.TextField(blank=True, null=True)
    tipo_dato = models.CharField(max_length=7, blank=True, null=True)
    grupo_config = models.CharField(max_length=50, blank=True, null=True)
    modificable_por_admin = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'configuraciones_sistema'


class Consultas(models.Model):
    id_consulta = models.AutoField(primary_key=True)
    id_estudiante = models.ForeignKey('Estudiantes', models.DO_NOTHING, db_column='id_estudiante')
    id_asignatura = models.ForeignKey(Asignaturas, models.DO_NOTHING, db_column='id_asignatura')
    id_categoria = models.ForeignKey(CategoriasTemas, models.DO_NOTHING, db_column='id_categoria', blank=True, null=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=7, blank=True, null=True)
    estado = models.CharField(max_length=10, blank=True, null=True)
    fecha_consulta = models.DateTimeField(blank=True, null=True)
    fecha_limite_respuesta = models.DateTimeField(blank=True, null=True)
    es_anonima = models.IntegerField(blank=True, null=True)
    adjunto_archivo = models.FileField(max_length=500, upload_to='adjuntos/', blank=True, null=True)
    tipo_consulta = models.CharField(max_length=21, blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'consultas'


class DocenteAsignatura(models.Model):
    id_docente_asignatura = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey('Docentes', models.DO_NOTHING, db_column='id_docente')
    id_asignatura = models.ForeignKey(Asignaturas, models.DO_NOTHING, db_column='id_asignatura')
    periodo_academico = models.CharField(max_length=20, blank=True, null=True)
    grupo = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'docente_asignatura'
        unique_together = (('id_docente', 'id_asignatura', 'periodo_academico', 'grupo'),)


class Docentes(models.Model):
    id_docente = models.AutoField(primary_key=True)
    id_usuario = models.OneToOneField('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    codigo_docente = models.CharField(unique=True, max_length=20)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    titulo_academico = models.CharField(max_length=200, blank=True, null=True)
    especialidades = models.TextField(blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    horario_atencion = models.TextField(blank=True, null=True)
    tiempo_respuesta_maximo = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'docentes'


class Estadisticas(models.Model):
    id_estadistica = models.AutoField(primary_key=True)
    tipo_estadistica = models.CharField(max_length=25)
    periodo = models.CharField(max_length=20, blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    datos_estadistica = models.JSONField()
    fecha_calculo = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'estadisticas'


class Estudiantes(models.Model):
    id_estudiante = models.AutoField(primary_key=True)
    id_usuario = models.OneToOneField('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    numero_matricula = models.CharField(unique=True, max_length=20)
    carrera = models.CharField(max_length=100, blank=True, null=True)
    semestre = models.IntegerField(blank=True, null=True)
    fecha_ingreso = models.DateField(blank=True, null=True)
    promedio_general = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'estudiantes'


class EvaluacionesRespuesta(models.Model):
    id_evaluacion = models.AutoField(primary_key=True)
    id_respuesta = models.OneToOneField('Respuestas', models.DO_NOTHING, db_column='id_respuesta')
    id_estudiante = models.ForeignKey(Estudiantes, models.DO_NOTHING, db_column='id_estudiante')
    calificacion = models.JSONField()
    comentario_evaluacion = models.TextField(blank=True, null=True)
    fue_util = models.IntegerField(blank=True, null=True)
    resolvio_duda = models.IntegerField(blank=True, null=True)
    fecha_evaluacion = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'evaluaciones_respuesta'


class LogsActividad(models.Model):
    id_log = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    tipo_evento = models.CharField(max_length=18)
    descripcion = models.TextField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    datos_adicionales = models.JSONField(blank=True, null=True)
    fecha_evento = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'logs_actividad'


class Notificaciones(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    id_usuario_destinatario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario_destinatario')
    tipo_notificacion = models.CharField(max_length=22)
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    id_referencia = models.IntegerField(blank=True, null=True)
    tipo_referencia = models.CharField(max_length=10, blank=True, null=True)
    leida = models.IntegerField(blank=True, null=True)
    enviada_email = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_leida = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'notificaciones'


class RecuperacionPasswords(models.Model):
    id_recuperacion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    token_recuperacion = models.CharField(unique=True, max_length=255)
    fecha_solicitud = models.DateTimeField(blank=True, null=True)
    fecha_expiracion = models.DateTimeField()
    utilizado = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'recuperacion_passwords'


class Respuestas(models.Model):
    id_respuesta = models.AutoField(primary_key=True)
    id_consulta = models.ForeignKey(Consultas, models.DO_NOTHING, db_column='id_consulta')
    id_docente = models.ForeignKey(Docentes, models.DO_NOTHING, db_column='id_docente')
    contenido_respuesta = models.TextField()
    tipo_respuesta = models.CharField(max_length=17, blank=True, null=True)
    adjunto_archivo = models.FileField(max_length=500, upload_to='adjuntos/', blank=True, null=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    tiempo_respuesta_horas = models.IntegerField(blank=True, null=True)
    calificacion_respuesta = models.JSONField(blank=True, null=True)
    es_respuesta_definitiva = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'respuestas'


class Seguimientos(models.Model):
    id_seguimiento = models.AutoField(primary_key=True)
    id_consulta = models.ForeignKey(Consultas, models.DO_NOTHING, db_column='id_consulta')
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    tipo_usuario = models.CharField(max_length=10)
    mensaje = models.TextField()
    adjunto_archivo = models.FileField(max_length=500, upload_to='adjuntos/', blank=True, null=True)
    fecha_seguimiento = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'seguimientos'


class SesionesUsuario(models.Model):
    id_sesion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    token_sesion = models.CharField(unique=True, max_length=255)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_expiracion = models.DateTimeField()
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    activa = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sesiones_usuario'


class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=100)
    password_hash = models.CharField(max_length=255)
    tipo_usuario = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    ultimo_acceso = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=10, blank=True, null=True)
    foto_perfil = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'usuarios'
