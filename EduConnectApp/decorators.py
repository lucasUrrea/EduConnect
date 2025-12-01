# decorators.py - Sistema de Control de Acceso Basado en Roles (RBAC)
"""
Sistema de autorización con decoradores para validar permisos de usuarios.
Implementa control de acceso granular diferenciando entre estudiantes, docentes y admin.
"""

from functools import wraps
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.utils import timezone
from .models import Usuarios, LogsActividad
import logging

logger = logging.getLogger(__name__)


def registrar_intento_acceso(request, accion, exitoso=True, detalles=''):
    """Registra intentos de acceso al sistema para auditoría de seguridad"""
    try:
        usuario_id = request.session.get('usuario_id')
        usuario = Usuarios.objects.get(id_usuario=usuario_id) if usuario_id else None
        
        LogsActividad.objects.create(
            id_usuario=usuario,
            tipo_evento='acceso_denegado' if not exitoso else 'acceso_permitido',
            descripcion=f"{accion} - {detalles}",
            ip_address=request.META.get('REMOTE_ADDR', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            fecha_evento=timezone.now()
        )
    except Exception as e:
        logger.error(f"Error al registrar intento de acceso: {str(e)}")


def login_required_custom(function):
    """
    Decorador que verifica si el usuario está autenticado.
    Similar a @login_required pero usa nuestro sistema de sesiones personalizado.
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated or 'usuario_id' not in request.session:
            registrar_intento_acceso(
                request, 
                f"Intento de acceso sin autenticación a {request.path}",
                exitoso=False,
                detalles="Usuario no autenticado"
            )
            
            if request.path.startswith('/api/'):
                return JsonResponse({
                    'error': 'No autenticado',
                    'message': 'Debes iniciar sesión para acceder a este recurso'
                }, status=401)
            
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        
        return function(request, *args, **kwargs)
    
    return wrap


def role_required(*allowed_roles):
    """
    Decorador que verifica si el usuario tiene uno de los roles permitidos.
    
    Uso:
        @role_required('docente')
        def vista_solo_docente(request):
            ...
        
        @role_required('estudiante', 'docente')
        def vista_estudiante_o_docente(request):
            ...
    
    Args:
        *allowed_roles: Lista de roles permitidos ('estudiante', 'docente', 'admin')
    """
    def decorator(function):
        @wraps(function)
        def wrap(request, *args, **kwargs):
            # Primero verificar autenticación
            if not request.user.is_authenticated or 'usuario_id' not in request.session:
                registrar_intento_acceso(
                    request,
                    f"Intento de acceso sin autenticación a {request.path}",
                    exitoso=False,
                    detalles=f"Roles requeridos: {', '.join(allowed_roles)}"
                )
                
                if request.path.startswith('/api/'):
                    return JsonResponse({
                        'error': 'No autenticado',
                        'message': 'Debes iniciar sesión'
                    }, status=401)
                
                messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')
            
            # Verificar rol del usuario
            tipo_usuario = request.session.get('tipo_usuario', '')
            
            # Admin siempre tiene acceso
            if request.user.is_superuser or request.user.is_staff:
                return function(request, *args, **kwargs)
            
            # Verificar si el usuario tiene el rol requerido
            if tipo_usuario not in allowed_roles:
                usuario_id = request.session.get('usuario_id')
                nombre = request.session.get('nombre_completo', 'Usuario')
                
                registrar_intento_acceso(
                    request,
                    f"Acceso denegado a {request.path}",
                    exitoso=False,
                    detalles=f"Usuario {nombre} (ID: {usuario_id}, Rol: {tipo_usuario}) intentó acceder. Roles requeridos: {', '.join(allowed_roles)}"
                )
                
                logger.warning(
                    f"Acceso denegado: Usuario {nombre} (tipo: {tipo_usuario}) "
                    f"intentó acceder a {request.path}. Roles permitidos: {allowed_roles}"
                )
                
                if request.path.startswith('/api/'):
                    return JsonResponse({
                        'error': 'Acceso denegado',
                        'message': f'No tienes permisos para acceder a este recurso. Rol requerido: {", ".join(allowed_roles)}'
                    }, status=403)
                
                messages.error(
                    request,
                    f'⛔ Acceso denegado. Esta página es solo para {", ".join(allowed_roles)}.'
                )
                return redirect('home')
            
            # Usuario autorizado
            return function(request, *args, **kwargs)
        
        return wrap
    return decorator


def estudiante_required(function):
    """
    Decorador específico para vistas que solo pueden acceder estudiantes.
    
    Uso:
        @estudiante_required
        def mi_vista_estudiante(request):
            ...
    """
    return role_required('estudiante')(function)


def docente_required(function):
    """
    Decorador específico para vistas que solo pueden acceder docentes.
    
    Uso:
        @docente_required
        def mi_vista_docente(request):
            ...
    """
    return role_required('docente')(function)


def docente_o_admin_required(function):
    """
    Decorador para vistas que pueden acceder docentes o administradores.
    
    Uso:
        @docente_o_admin_required
        def gestionar_consultas(request):
            ...
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            return function(request, *args, **kwargs)
        
        return role_required('docente')(function)(request, *args, **kwargs)
    
    return wrap


def permission_required_custom(permission_name):
    """
    Decorador para verificar permisos específicos basados en acciones.
    
    Permisos disponibles:
    - 'crear_consulta': Crear nuevas consultas
    - 'responder_consulta': Responder consultas
    - 'eliminar_consulta': Eliminar consultas
    - 'ver_todas_consultas': Ver consultas de todos los estudiantes
    - 'gestionar_asignaturas': Administrar asignaturas
    - 'ver_reportes': Ver reportes y estadísticas
    - 'exportar_datos': Exportar datos del sistema
    
    Uso:
        @permission_required_custom('responder_consulta')
        def responder(request, id_consulta):
            ...
    """
    # Mapeo de permisos por rol
    PERMISSIONS_MAP = {
        'estudiante': {
            'crear_consulta',
            'ver_mis_consultas',
            'editar_mi_consulta',
            'eliminar_mi_consulta',
            'ver_mi_perfil',
        },
        'docente': {
            'responder_consulta',
            'ver_todas_consultas',
            'ver_consultas_asignatura',
            'cerrar_consulta',
            'ver_reportes',
            'exportar_datos',
            'ver_perfil_estudiante',
            'gestionar_respuestas',
        },
    }
    
    def decorator(function):
        @wraps(function)
        def wrap(request, *args, **kwargs):
            if not request.user.is_authenticated or 'usuario_id' not in request.session:
                if request.path.startswith('/api/'):
                    return JsonResponse({
                        'error': 'No autenticado'
                    }, status=401)
                messages.error(request, 'Debes iniciar sesión.')
                return redirect('login')
            
            # Admin tiene todos los permisos
            if request.user.is_superuser or request.user.is_staff:
                return function(request, *args, **kwargs)
            
            tipo_usuario = request.session.get('tipo_usuario', '')
            user_permissions = PERMISSIONS_MAP.get(tipo_usuario, set())
            
            if permission_name not in user_permissions:
                registrar_intento_acceso(
                    request,
                    f"Permiso denegado: {permission_name}",
                    exitoso=False,
                    detalles=f"Usuario tipo {tipo_usuario} intentó {permission_name} en {request.path}"
                )
                
                logger.warning(
                    f"Permiso denegado: Usuario {tipo_usuario} "
                    f"intentó ejecutar '{permission_name}' en {request.path}"
                )
                
                if request.path.startswith('/api/'):
                    return JsonResponse({
                        'error': 'Permiso denegado',
                        'message': f'No tienes permiso para: {permission_name}'
                    }, status=403)
                
                messages.error(request, f'⛔ No tienes permiso para realizar esta acción.')
                return redirect('home')
            
            return function(request, *args, **kwargs)
        
        return wrap
    return decorator


def ajax_login_required(function):
    """
    Decorador específico para endpoints AJAX/API que requieren autenticación.
    Siempre devuelve JSON en lugar de redirigir.
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated or 'usuario_id' not in request.session:
            return JsonResponse({
                'error': 'No autenticado',
                'message': 'Tu sesión ha expirado. Por favor, inicia sesión nuevamente.',
                'redirect': '/login/'
            }, status=401)
        
        return function(request, *args, **kwargs)
    
    return wrap


def can_access_consulta(function):
    """
    Decorador que verifica si el usuario tiene permiso para acceder a una consulta específica.
    
    Reglas:
    - Estudiante: Solo puede ver sus propias consultas
    - Docente: Puede ver consultas de asignaturas que imparte
    - Admin: Puede ver todas
    
    Uso:
        @can_access_consulta
        def detalle_consulta(request, id_consulta):
            ...
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        from .models import Consultas, DocenteAsignatura
        
        if not request.user.is_authenticated or 'usuario_id' not in request.session:
            if request.path.startswith('/api/'):
                return JsonResponse({'error': 'No autenticado'}, status=401)
            messages.error(request, 'Debes iniciar sesión.')
            return redirect('login')
        
        # Admin tiene acceso total
        if request.user.is_superuser or request.user.is_staff:
            return function(request, *args, **kwargs)
        
        # Obtener ID de la consulta desde kwargs o args
        id_consulta = kwargs.get('id_consulta') or kwargs.get('pk')
        if not id_consulta:
            return JsonResponse({'error': 'ID de consulta no proporcionado'}, status=400)
        
        try:
            consulta = Consultas.objects.get(id_consulta=id_consulta)
        except Consultas.DoesNotExist:
            return JsonResponse({'error': 'Consulta no encontrada'}, status=404)
        
        usuario_id = request.session.get('usuario_id')
        tipo_usuario = request.session.get('tipo_usuario')
        
        tiene_acceso = False
        
        if tipo_usuario == 'estudiante':
            # Estudiante solo ve sus consultas
            tiene_acceso = (consulta.id_estudiante.id_usuario.id_usuario == usuario_id)
        
        elif tipo_usuario == 'docente':
            # Docente ve consultas de sus asignaturas
            from .models import Docentes
            try:
                docente = Docentes.objects.get(id_usuario__id_usuario=usuario_id)
                asignaturas_docente = DocenteAsignatura.objects.filter(
                    id_docente=docente
                ).values_list('id_asignatura', flat=True)
                
                tiene_acceso = consulta.id_asignatura.id_asignatura in asignaturas_docente
            except Docentes.DoesNotExist:
                tiene_acceso = False
        
        if not tiene_acceso:
            registrar_intento_acceso(
                request,
                f"Acceso denegado a consulta #{id_consulta}",
                exitoso=False,
                detalles=f"Usuario {usuario_id} ({tipo_usuario}) intentó acceder"
            )
            
            if request.path.startswith('/api/'):
                return JsonResponse({
                    'error': 'Acceso denegado',
                    'message': 'No tienes permiso para ver esta consulta'
                }, status=403)
            
            messages.error(request, '⛔ No tienes permiso para ver esta consulta.')
            return redirect('home')
        
        return function(request, *args, **kwargs)
    
    return wrap
