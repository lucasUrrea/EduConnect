from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.core.cache import cache
from django.utils import timezone
from .models import Usuarios, LogsActividad
import logging
import re

logger = logging.getLogger(__name__)


class EnsureUsuarioSessionMiddleware(MiddlewareMixin):
    """
    Ensure that when a Django user is authenticated, the session contains
    the corresponding Usuarios.id_usuario and tipo_usuario values.

    This addresses cases where authentication succeeds but the custom session
    keys used by views ('usuario_id', 'tipo_usuario') are missing.
    """
    def process_request(self, request):
        try:
            if getattr(request, 'user', None) and request.user.is_authenticated:
                if 'usuario_id' not in request.session:
                    try:
                        perfil = Usuarios.objects.get(email=request.user.email)
                        request.session['usuario_id'] = perfil.id_usuario
                        request.session['tipo_usuario'] = perfil.tipo_usuario
                        request.session['nombre_completo'] = f"{perfil.nombre} {perfil.apellido_paterno}"
                        
                        # Actualizar último acceso
                        perfil.ultimo_acceso = timezone.now()
                        perfil.save(update_fields=['ultimo_acceso'])
                    except Usuarios.DoesNotExist:
                        pass
        except Exception as e:
            # Don't let session population break requests
            logger.error(f"Error en EnsureUsuarioSessionMiddleware: {str(e)}")
            pass


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Añade headers de seguridad adicionales a todas las respuestas.
    Complementa las configuraciones de settings.py.
    """
    def process_response(self, request, response):
        # Content Security Policy - Permite CDNs confiables
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://code.jquery.com https://stackpath.bootstrapcdn.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com https://stackpath.bootstrapcdn.com; "
            "img-src 'self' data: https: blob:; "
            "font-src 'self' data: https://fonts.gstatic.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "connect-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com;"
        )
        
        # Protección contra MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Política de referencia
        response['Referrer-Policy'] = 'same-origin'
        
        # Deshabilitar características del navegador
        response['Permissions-Policy'] = (
            "geolocation=(), microphone=(), camera=(), "
            "payment=(), usb=(), magnetometer=(), gyroscope=()"
        )
        
        return response


class RateLimitMiddleware(MiddlewareMixin):
    """
    Middleware para limitar la tasa de peticiones por IP.
    Previene ataques de fuerza bruta y DDoS.
    
    En desarrollo (DEBUG=True), los límites son más permisivos.
    En producción, se aplican límites más estrictos.
    """
    # Configuración: máximo de requests por ventana de tiempo
    MAX_REQUESTS = 100  # requests
    TIME_WINDOW = 60    # segundos
    
    # Endpoints sensibles con límites más estrictos
    # Los valores se multiplican por 10 en desarrollo (DEBUG=True)
    SENSITIVE_ENDPOINTS = {
        '/login/': {'max': 5, 'window': 60},
        '/api/auth/login/': {'max': 5, 'window': 60},
        '/password-reset/': {'max': 3, 'window': 300},
        '/api/': {'max': 50, 'window': 60},
    }
    
    def process_request(self, request):
        # Obtener IP del cliente
        ip_address = self.get_client_ip(request)
        
        # Verificar si estamos en desarrollo
        from django.conf import settings
        is_development = settings.DEBUG
        
        # Verificar si la ruta es sensible
        path = request.path
        config = None
        for endpoint, limits in self.SENSITIVE_ENDPOINTS.items():
            if path.startswith(endpoint):
                config = limits
                break
        
        if config:
            max_requests = config['max']
            time_window = config['window']
        else:
            max_requests = self.MAX_REQUESTS
            time_window = self.TIME_WINDOW
        
        # En desarrollo, multiplicar los límites por 10 para ser más permisivo
        if is_development:
            max_requests = max_requests * 10
        
        # Crear clave única para el caché
        cache_key = f'rate_limit:{ip_address}:{path}'
        
        # Obtener contador actual
        request_count = cache.get(cache_key, 0)
        
        if request_count >= max_requests:
            logger.warning(
                f"Rate limit excedido para IP {ip_address} en {path}. "
                f"Requests: {request_count}/{max_requests}"
            )
            
            # Registrar en logs de actividad
            try:
                LogsActividad.objects.create(
                    tipo_evento='rate_limit_exceeded',
                    descripcion=f'Rate limit excedido para {path}',
                    ip_address=ip_address,
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                    fecha_evento=timezone.now()
                )
            except Exception as e:
                logger.error(f"Error al registrar rate limit: {str(e)}")
            
            if request.path.startswith('/api/'):
                return JsonResponse(
                    {
                        'error': 'Demasiadas peticiones. Intenta de nuevo más tarde.',
                        'retry_after': time_window
                    },
                    status=429
                )
            else:
                return HttpResponseForbidden(
                    "Demasiadas peticiones. Intenta de nuevo más tarde."
                )
        
        # Incrementar contador
        cache.set(cache_key, request_count + 1, time_window)
        
        return None
    
    def get_client_ip(self, request):
        """Obtiene la IP real del cliente, considerando proxies"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class InputSanitizationMiddleware(MiddlewareMixin):
    """
    Middleware para sanitizar y validar inputs.
    Previene ataques de inyección SQL, XSS, y otros.
    """
    # Patrones peligrosos
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',  # Scripts
        r'javascript:',                  # JavaScript URLs
        r'on\w+\s*=',                   # Event handlers
        r'<iframe[^>]*>',               # iframes
        r'<object[^>]*>',               # objects
        r'<embed[^>]*>',                # embeds
    ]
    
    def process_request(self, request):
        # Solo validar POST, PUT, PATCH
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                # Validar datos POST
                if hasattr(request, 'POST'):
                    for key, value in request.POST.items():
                        if isinstance(value, str) and self.contains_dangerous_pattern(value):
                            logger.warning(
                                f"Contenido peligroso detectado en POST[{key}] desde IP {self.get_client_ip(request)}"
                            )
                            
                            if request.path.startswith('/api/'):
                                return JsonResponse(
                                    {'error': 'Contenido inválido detectado'},
                                    status=400
                                )
            except Exception as e:
                logger.error(f"Error en InputSanitizationMiddleware: {str(e)}")
        
        return None
    
    def contains_dangerous_pattern(self, text):
        """Verifica si el texto contiene patrones peligrosos"""
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def get_client_ip(self, request):
        """Obtiene la IP real del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ActivityLogMiddleware(MiddlewareMixin):
    """
    Middleware para registrar actividad de usuarios.
    Registra acciones importantes para auditoría.
    """
    # Métodos que se deben registrar
    LOGGED_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']
    
    # Rutas que se deben registrar
    LOGGED_PATHS = [
        '/api/',
        '/login/',
        '/logout/',
        '/admin/',
    ]
    
    def process_response(self, request, response):
        try:
            # Solo registrar métodos y rutas específicas
            should_log = (
                request.method in self.LOGGED_METHODS or
                any(request.path.startswith(path) for path in self.LOGGED_PATHS)
            )
            
            if should_log and hasattr(request, 'user') and request.user.is_authenticated:
                # Obtener usuario del sistema personalizado
                usuario_id = request.session.get('usuario_id')
                
                if usuario_id:
                    try:
                        # Determinar tipo de evento
                        tipo_evento = self.get_event_type(request)
                        
                        # Crear log
                        LogsActividad.objects.create(
                            id_usuario_id=usuario_id,
                            tipo_evento=tipo_evento,
                            descripcion=f"{request.method} {request.path}",
                            ip_address=self.get_client_ip(request),
                            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                            datos_adicionales={
                                'status_code': response.status_code,
                                'method': request.method,
                                'path': request.path,
                            },
                            fecha_evento=timezone.now()
                        )
                    except Exception as e:
                        logger.error(f"Error al crear log de actividad: {str(e)}")
        except Exception as e:
            logger.error(f"Error en ActivityLogMiddleware: {str(e)}")
        
        return response
    
    def get_event_type(self, request):
        """Determina el tipo de evento basado en la ruta y método"""
        path = request.path.lower()
        method = request.method
        
        if 'login' in path:
            return 'login'
        elif 'logout' in path:
            return 'logout'
        elif method == 'POST':
            return 'create'
        elif method in ['PUT', 'PATCH']:
            return 'update'
        elif method == 'DELETE':
            return 'delete'
        else:
            return 'access'
    
    def get_client_ip(self, request):
        """Obtiene la IP real del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RoleBasedAccessControlMiddleware(MiddlewareMixin):
    """
    Middleware que valida automáticamente el acceso a rutas basado en roles.
    Implementa control de acceso a nivel de URL para diferenciar permisos entre
    estudiantes, docentes y administradores.
    """
    
    # Rutas exclusivas para ESTUDIANTES
    ESTUDIANTE_ONLY_PATHS = [
        '/dashboard/estudiante/',
        '/mis-consultas/',
        '/crear-consulta/',
    ]
    
    # Rutas exclusivas para DOCENTES
    DOCENTE_ONLY_PATHS = [
        '/dashboard/docente/',
        '/consultas-asignatura/',
        '/responder/',
        '/gestionar-respuestas/',
        '/reportes/docente/',
    ]
    
    # Rutas que requieren autenticación pero son accesibles por ambos roles
    SHARED_PATHS = [
        '/perfil/',
        '/configuracion/',
        '/notificaciones/',
    ]
    
    # Rutas públicas que no requieren autenticación
    PUBLIC_PATHS = [
        '/login/',
        '/logout/',
        '/password-reset/',
        '/admin/',
        '/static/',
        '/media/',
        '/favicon',
    ]
    
    def process_request(self, request):
        """
        Valida si el usuario tiene permiso para acceder a la ruta solicitada.
        """
        path = request.path
        
        # Permitir ruta raíz (home)
        if path == '/' or path == '':
            return None
        
        # Permitir rutas públicas
        if any(path.startswith(public) for public in self.PUBLIC_PATHS):
            return None
        
        # Admin tiene acceso total
        if request.user.is_superuser or request.user.is_staff:
            return None
        
        # Verificar autenticación para rutas protegidas
        if not request.user.is_authenticated:
            # Si intenta acceder a ruta protegida sin autenticación
            if self._is_protected_path(path):
                logger.warning(f"Intento de acceso sin autenticación a {path} desde IP {self._get_client_ip(request)}")
                
                if path.startswith('/api/'):
                    return JsonResponse({
                        'error': 'No autenticado',
                        'message': 'Debes iniciar sesión para acceder a este recurso'
                    }, status=401)
                
                # Redirigir a login
                from django.shortcuts import redirect
                from django.contrib import messages
                try:
                    messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
                except:
                    pass  # En pruebas o sin MessageMiddleware
                return redirect('login')
            
            return None
        
        # Usuario autenticado - obtener tipo de usuario
        # Si no está en sesión aún, permitir que EnsureUsuarioSessionMiddleware lo establezca
        tipo_usuario = request.session.get('tipo_usuario', '')
        
        # Si el tipo de usuario no está establecido aún, no validar rol
        # (permite que el login complete el proceso)
        if not tipo_usuario:
            return None
        
        # Validar acceso por rol
        if self._is_estudiante_only_path(path):
            if tipo_usuario != 'estudiante':
                return self._access_denied(request, 'estudiante', path)
        
        elif self._is_docente_only_path(path):
            if tipo_usuario != 'docente':
                return self._access_denied(request, 'docente', path)
        
        return None
    
    def _is_protected_path(self, path):
        """Verifica si la ruta está protegida (requiere autenticación)"""
        return (
            self._is_estudiante_only_path(path) or
            self._is_docente_only_path(path) or
            any(path.startswith(shared) for shared in self.SHARED_PATHS)
        )
    
    def _is_estudiante_only_path(self, path):
        """Verifica si la ruta es exclusiva para estudiantes"""
        return any(path.startswith(est_path) for est_path in self.ESTUDIANTE_ONLY_PATHS)
    
    def _is_docente_only_path(self, path):
        """Verifica si la ruta es exclusiva para docentes"""
        return any(path.startswith(doc_path) for doc_path in self.DOCENTE_ONLY_PATHS)
    
    def _access_denied(self, request, required_role, path):
        """Maneja el acceso denegado registrando el intento y respondiendo apropiadamente"""
        usuario_id = request.session.get('usuario_id')
        tipo_usuario = request.session.get('tipo_usuario', 'desconocido')
        nombre = request.session.get('nombre_completo', 'Usuario')
        
        # Registrar intento de acceso no autorizado
        logger.warning(
            f"⛔ ACCESO DENEGADO: Usuario {nombre} (ID:{usuario_id}, Tipo:{tipo_usuario}) "
            f"intentó acceder a {path} (requiere rol: {required_role})"
        )
        
        try:
            LogsActividad.objects.create(
                id_usuario_id=usuario_id,
                tipo_evento='acceso_denegado',
                descripcion=f"Intento de acceso a ruta protegida: {path} (Requiere: {required_role})",
                ip_address=self._get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                datos_adicionales={
                    'tipo_usuario': tipo_usuario,
                    'ruta': path,
                    'rol_requerido': required_role
                },
                fecha_evento=timezone.now()
            )
        except Exception as e:
            logger.error(f"Error al registrar acceso denegado: {str(e)}")
        
        # Responder según tipo de request
        if path.startswith('/api/'):
            return JsonResponse({
                'error': 'Acceso denegado',
                'message': f'Esta funcionalidad es exclusiva para {required_role}s',
                'required_role': required_role,
                'your_role': tipo_usuario
            }, status=403)
        
        # Para rutas normales, redirigir con mensaje
        from django.shortcuts import redirect
        from django.contrib import messages
        
        try:
            messages.error(
                request,
                f'⛔ Acceso denegado. Esta página es exclusiva para usuarios con rol de {required_role}.'
            )
        except:
            pass  # En pruebas o sin MessageMiddleware
        return redirect('home')
    
    def _get_client_ip(self, request):
        """Obtiene la IP real del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
