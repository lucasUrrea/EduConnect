from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import *
from django.utils import timezone
from datetime import datetime, timedelta
from .forms import ConsultaForm, RespuestaForm
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

logger = logging.getLogger(__name__)


def _ensure_session_from_authenticated(request):
    """If a Django user is authenticated but session lacks usuario_id, try to fill it from Usuarios."""
    if request.user.is_authenticated and 'usuario_id' not in request.session:
        try:
            perfil = Usuarios.objects.get(email=request.user.email)
            request.session['usuario_id'] = perfil.id_usuario
            request.session['tipo_usuario'] = perfil.tipo_usuario
            request.session['nombre_completo'] = f"{perfil.nombre} {perfil.apellido_paterno}"
        except Usuarios.DoesNotExist:
            pass

def home(request):
    """Vista principal: si el usuario está autenticado mostramos una versión personalizada
    en lugar de redirigir inmediatamente (evitamos que docentes vayan directo al dashboard).
    """
    contexto = {}
    if request.user.is_authenticated:
        try:
            usuario = Usuarios.objects.get(email=request.user.email)
            request.session['usuario_id'] = usuario.id_usuario
            request.session['tipo_usuario'] = usuario.tipo_usuario
            request.session['nombre_completo'] = f"{usuario.nombre} {usuario.apellido_paterno}"

            # Provide a light overview for authenticated users
            if usuario.tipo_usuario == 'estudiante':
                total = Consultas.objects.filter(id_estudiante__id_usuario=usuario.id_usuario).count()
                contexto.update({'welcome_message': f"Bienvenido, {usuario.nombre}", 'total_consultas': total, 'tipo_usuario':'estudiante'})
            elif usuario.tipo_usuario == 'docente':
                # Count pending consultas across their asignaturas
                try:
                    docente = Docentes.objects.get(id_usuario=usuario)
                    asign_ids = DocenteAsignatura.objects.filter(id_docente=docente).values_list('id_asignatura', flat=True)
                    pendientes = Consultas.objects.filter(id_asignatura__in=asign_ids, estado='pendiente').count()
                    contexto.update({'welcome_message': f"Bienvenido, Prof. {usuario.apellido_paterno}", 'pendientes': pendientes, 'tipo_usuario':'docente'})
                except Docentes.DoesNotExist:
                    contexto.update({'welcome_message': f"Bienvenido, {usuario.nombre}"})
        except Usuarios.DoesNotExist:
            pass

    return render(request, 'EduConnectApp/home.html', contexto)

@csrf_protect
def login_view(request):
    """Vista de login personalizada"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        # Intentar autenticación con Django User primero
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)

            # Cargar datos del perfil desde Usuarios
            try:
                perfil = Usuarios.objects.get(email=user.email)
                request.session['usuario_id'] = perfil.id_usuario
                request.session['tipo_usuario'] = perfil.tipo_usuario
                request.session['nombre_completo'] = f"{perfil.nombre} {perfil.apellido_paterno}"
            except Usuarios.DoesNotExist:
                pass
            
            # Redirigir según tipo de usuario
            if user.is_staff or user.is_superuser:
                return redirect('/admin/')
            
            tipo = request.session.get('tipo_usuario')
            if tipo == 'estudiante':
                return redirect('dashboard_estudiante')
            elif tipo == 'docente':
                return redirect('dashboard_docente')
            else:
                return redirect('home')
        
        # Si falla, intentar con tabla Usuarios personalizada
        try:
            usuario = Usuarios.objects.get(email=email)
            if check_password(password, usuario.password_hash) and usuario.estado == 'activo':
                # Crear o actualizar Django User
                django_user, created = User.objects.get_or_create(
                    username=usuario.email, 
                    defaults={
                        'email': usuario.email,
                        'first_name': usuario.nombre,
                        'last_name': usuario.apellido_paterno,
                    }
                )
                if created:
                    django_user.set_password(password)
                    django_user.save()
                
                # Autenticar con Django
                django_user = authenticate(request, username=usuario.email, password=password)
                if django_user:
                    auth_login(request, django_user)

                # Guardar datos en sesión
                request.session['usuario_id'] = usuario.id_usuario
                request.session['tipo_usuario'] = usuario.tipo_usuario
                request.session['nombre_completo'] = f"{usuario.nombre} {usuario.apellido_paterno}"

                # Verificar si es staff
                try:
                    du = User.objects.get(username=usuario.email)
                    if du.is_staff or du.is_superuser:
                        return redirect('/admin/')
                except User.DoesNotExist:
                    pass

                if usuario.tipo_usuario == 'estudiante':
                    return redirect('dashboard_estudiante')
                else:
                    return redirect('dashboard_docente')
            else:
                messages.error(request, 'Credenciales inválidas o usuario inactivo')
        except Usuarios.DoesNotExist:
            messages.error(request, 'Credenciales inválidas')
    
    # render login page (GET) or re-show form after POST errors
    return render(request, 'EduConnectApp/login.html')


@csrf_protect
def login_docente(request):
    """Inicio de sesión específico para docentes"""
    # Ensure CSRF cookie is present when serving the form
    # fetch token so cookie is set and we can pass it to the template for diagnostics
    token = None
    if request.method == 'GET':
        token = get_token(request)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # intentar autenticación Django
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # verificar que exista perfil docente
            try:
                perfil = Usuarios.objects.get(email=user.email)
                if perfil.tipo_usuario != 'docente':
                    messages.error(request, 'Cuenta no es de docente')
                    return redirect('login_docente')
                auth_login(request, user)
                request.session['usuario_id'] = perfil.id_usuario
                request.session['tipo_usuario'] = perfil.tipo_usuario
                request.session['nombre_completo'] = f"{perfil.nombre} {perfil.apellido_paterno}"
                return redirect('panel_docente')
            except Usuarios.DoesNotExist:
                messages.error(request, 'Perfil docente no encontrado')
        else:
            messages.error(request, 'Credenciales inválidas')

    # Render docente login page
    return render(request, 'EduConnectApp/login_docente.html')


def panel_docente(request):
    """Interfaz exclusiva para docentes: listado de alumnos y preguntas"""
    _ensure_session_from_authenticated(request)
    if 'usuario_id' not in request.session or request.session.get('tipo_usuario') != 'docente':
        return redirect('login_docente')

    usuario_id = request.session['usuario_id']
    docente = get_object_or_404(Docentes, id_usuario=usuario_id)

    # obtener asignaturas
    asignaturas_docente = DocenteAsignatura.objects.filter(id_docente=docente).select_related('id_asignatura')
    asign_ids = [da.id_asignatura.id_asignatura for da in asignaturas_docente]

    # estudiantes que han hecho consultas en sus asignaturas
    consultas = Consultas.objects.filter(id_asignatura__in=asign_ids).select_related('id_estudiante__id_usuario', 'id_asignatura').order_by('-fecha_consulta')[:50]

    # alumnos únicos
    estudiantes_ids = list({c.id_estudiante.id_estudiante for c in consultas})
    estudiantes = Estudiantes.objects.filter(id_estudiante__in=estudiantes_ids).select_related('id_usuario')

    context = {
        'docente': docente,
        'asignaturas_docente': asignaturas_docente,
        'consultas_recientes': consultas,
        'estudiantes': estudiantes,
    }
    return render(request, 'EduConnectApp/panel_docente.html', context)

def logout_view(request):
    """Vista de logout"""
    request.session.flush()
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('home')

def dashboard_estudiante(request):
    """Dashboard principal para estudiantes"""
    if 'usuario_id' not in request.session or request.session.get('tipo_usuario') != 'estudiante':
        return redirect('login')
    
    usuario_id = request.session['usuario_id']
    estudiante = get_object_or_404(Estudiantes, id_usuario=usuario_id)
    
    # Obtener consultas del estudiante
    consultas_recientes = Consultas.objects.filter(
        id_estudiante=estudiante.id_estudiante
    ).order_by('-fecha_consulta')[:5]
    # Log for diagnostics
    try:
        logger.debug(f"dashboard_estudiante user={usuario_id} estudiante={estudiante.id_estudiante} consultas_recientes={consultas_recientes.count()}")
    except Exception:
        pass
    
    # Obtener todas las asignaturas disponibles
    asignaturas = Asignaturas.objects.filter(estado='activo').order_by('nombre_asignatura')
    
    # Obtener todas las categorías disponibles
    categorias = CategoriasTemas.objects.select_related('id_asignatura').order_by('id_asignatura__nombre_asignatura', 'nombre_categoria')
    
    # Estadísticas
    total_consultas = Consultas.objects.filter(id_estudiante=estudiante.id_estudiante).count()
    consultas_pendientes = Consultas.objects.filter(
        id_estudiante=estudiante.id_estudiante,
        estado='pendiente'
    ).count()
    consultas_respondidas = Consultas.objects.filter(
        id_estudiante=estudiante.id_estudiante,
        estado='respondida'
    ).count()
    
    context = {
        'estudiante': estudiante,
        'consultas_recientes': consultas_recientes,
        'total_consultas': total_consultas,
        'consultas_pendientes': consultas_pendientes,
        'consultas_respondidas': consultas_respondidas,
        'asignaturas': asignaturas,
        'categorias': categorias,
    }
    
    return render(request, 'EduConnectApp/dashboard_estudiante.html', context)


def mis_consultas(request):
    _ensure_session_from_authenticated(request)
    if 'usuario_id' not in request.session:
        return redirect('login')

    usuario_id = request.session['usuario_id']
    estudiante = get_object_or_404(Estudiantes, id_usuario=usuario_id)
    consultas = Consultas.objects.filter(id_estudiante=estudiante).order_by('-fecha_consulta')
    try:
        logger.debug(f"mis_consultas user={usuario_id} estudiante={estudiante.id_estudiante} consultas_total={consultas.count()}")
    except Exception:
        pass
    return render(request, 'EduConnectApp/mis_consultas.html', {'consultas': consultas})


def mi_progreso(request):
    _ensure_session_from_authenticated(request)
    if 'usuario_id' not in request.session:
        return redirect('login')

    # ejemplo simple de progreso: número de consultas por mes
    usuario_id = request.session['usuario_id']
    estudiante = get_object_or_404(Estudiantes, id_usuario=usuario_id)
    consultas = Consultas.objects.filter(id_estudiante=estudiante)
    total = consultas.count()
    respondidas = consultas.filter(estado='respondida').count()
    # preparar datos por mes (ultimos 6 meses)
    today = timezone.now().date()
    labels = []
    values = []
    for i in range(5, -1, -1):
        # compute target month by subtracting i months
        target_month = (today.replace(day=1) - timedelta(days=30*i))
        year = target_month.year
        month_num = target_month.month
        # contar consultas en ese mes
        count = consultas.filter(fecha_consulta__year=year, fecha_consulta__month=month_num).count()
        labels.append(target_month.strftime('%b %Y'))
        values.append(count)

    # por asignatura (top 6)
    asignatura_counts = (
        consultas.values('id_asignatura__nombre_asignatura')
        .annotate(count=Count('id_asignatura'))
        .order_by('-count')[:6]
    )
    asign_labels = [a['id_asignatura__nombre_asignatura'] for a in asignatura_counts]
    asign_values = [a['count'] for a in asignatura_counts]

    # donut: respondidas vs sin responder
    sin_responder = total - respondidas

    # porcentaje de respuestas
    if total > 0:
        percent_respuestas = int((respondidas / total) * 100)
    else:
        percent_respuestas = 0

    contexto = {
        'total': total,
        'respondidas': respondidas,
        'percent_respuestas': percent_respuestas,
        'estudiante': estudiante,
        'labels': labels,
        'values': values,
        'asign_labels': asign_labels,
        'asign_values': asign_values,
        'donut_labels': ['Respondidas', 'Sin responder'],
        'donut_values': [respondidas, sin_responder],
    }
    return render(request, 'EduConnectApp/mi_progreso.html', contexto)


def editar_perfil(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    usuario_id = request.session['usuario_id']
    usuario = get_object_or_404(Usuarios, id_usuario=usuario_id)

    from .forms import ProfileForm

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            usuario.nombre = form.cleaned_data['nombre']
            usuario.apellido_paterno = form.cleaned_data['apellido_paterno']
            usuario.telefono = form.cleaned_data.get('telefono')
            usuario.save()
            messages.success(request, 'Perfil actualizado')
            return redirect('dashboard_estudiante' if usuario.tipo_usuario=='estudiante' else 'dashboard_docente')
    else:
        form = ProfileForm(initial={'nombre': usuario.nombre, 'apellido_paterno': usuario.apellido_paterno, 'telefono': usuario.telefono})

    return render(request, 'EduConnectApp/perfil_edit.html', {'form': form, 'usuario': usuario})

def dashboard_docente(request):
    """Dashboard principal para docentes"""
    if 'usuario_id' not in request.session or request.session.get('tipo_usuario') != 'docente':
        return redirect('login')
    
    usuario_id = request.session['usuario_id']
    usuario = get_object_or_404(Usuarios, id_usuario=usuario_id)
    docente = get_object_or_404(Docentes, id_usuario=usuario)
    
    # Obtener asignaturas del docente
    asignaturas_docente = DocenteAsignatura.objects.filter(
        id_docente=docente.id_docente
    ).select_related('id_asignatura')
    
    # Mostrar TODAS las consultas (no solo las de las asignaturas del docente)
    consultas_pendientes = Consultas.objects.filter(
        estado='pendiente'
    ).select_related('id_estudiante__id_usuario', 'id_asignatura').order_by('-fecha_consulta')
    
    # Respuestas guardadas por el docente (que puede editar)
    respuestas_guardadas = Respuestas.objects.filter(
        id_docente=docente.id_docente
    ).select_related(
        'id_consulta__id_estudiante__id_usuario',
        'id_consulta__id_asignatura'
    ).order_by('-fecha_respuesta')[:20]  # Últimas 20 respuestas
    
    # Estadísticas
    total_consultas_pendientes = consultas_pendientes.count()
    consultas_respondidas_hoy = Respuestas.objects.filter(
        id_docente=docente.id_docente,
        fecha_respuesta__date=timezone.now().date()
    ).count()
    total_respuestas_guardadas = Respuestas.objects.filter(
        id_docente=docente.id_docente
    ).count()
    
    context = {
        'docente': docente,
        'consultas_pendientes': consultas_pendientes,
        'respuestas_guardadas': respuestas_guardadas,
        'asignaturas_docente': asignaturas_docente,
        'total_consultas_pendientes': total_consultas_pendientes,
        'consultas_respondidas_hoy': consultas_respondidas_hoy,
        'total_respuestas_guardadas': total_respuestas_guardadas,
    }
    
    return render(request, 'EduConnectApp/dashboard_docente.html', context)

def crear_consulta(request):
    """Vista para que los estudiantes creen nuevas consultas"""
    if 'usuario_id' not in request.session or request.session.get('tipo_usuario') != 'estudiante':
        return redirect('login')
    
    usuario_id = request.session['usuario_id']
    estudiante = get_object_or_404(Estudiantes, id_usuario=usuario_id)
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST, request.FILES)
        # minimal logging only
        try:
            logger.debug(f"crear_consulta POST keys={list(request.POST.keys())} FILES keys={list(request.FILES.keys())}")
        except Exception:
            pass
        # Note: temporary test-only logging removed. Use normal logger.debug above if needed.
        # Debug: log incoming files and posted keys to diagnose file save issues
        try:
            logger.debug(f"crear_consulta POST keys={list(request.POST.keys())} FILES keys={list(request.FILES.keys())}")
        except Exception:
            logger.debug("crear_consulta POST - unable to list POST/FILES keys")
        if form.is_valid():
            # Build Consulta manually from cleaned_data to ensure file assignment
            cd = form.cleaned_data
            consulta = Consultas(
                id_estudiante=estudiante,
                id_asignatura=cd.get('id_asignatura'),
                id_categoria=cd.get('id_categoria'),
                titulo=cd.get('titulo'),
                descripcion=cd.get('descripcion'),
                prioridad=cd.get('prioridad'),
                estado='pendiente',  # Establecer estado inicial
                fecha_consulta=timezone.now()
            )

            # Assign uploaded file if present
            if request.FILES.get('adjunto_archivo'):
                try:
                    file = request.FILES['adjunto_archivo']
                    # Save using default_storage to ensure file is written in test and production
                    path = default_storage.save(f"adjuntos/{file.name}", ContentFile(file.read()))
                    consulta.adjunto_archivo = path
                except Exception:
                    logger.exception('crear_consulta: error saving uploaded file')

            consulta.save()
            # After save, log the stored filename/path
            try:
                logger.debug(f"crear_consulta: after save adjunto_archivo.name={getattr(consulta.adjunto_archivo, 'name', None)}")
            except Exception:
                logger.debug("crear_consulta: after save unable to read adjunto_archivo")
            # If file was saved, include filename in the success message
            try:
                fname = getattr(consulta.adjunto_archivo, 'name', None)
                if fname:
                    messages.success(request, f'Consulta creada exitosamente. Archivo guardado: {fname}')
                else:
                    messages.success(request, 'Consulta creada exitosamente')
            except Exception:
                messages.success(request, 'Consulta creada exitosamente')
            return redirect('dashboard_estudiante')
        else:
            # Log form errors for debugging (development)
            try:
                logger.debug(f"crear_consulta: form errors={form.errors.as_json()} POST_keys={list(request.POST.keys())} FILES_keys={list(request.FILES.keys())}")
            except Exception:
                logger.debug(f"crear_consulta: form invalid, errors={form.errors}")
            messages.error(request, 'Por favor corrija los errores del formulario')
    
    # Obtener asignaturas y categorías para el formulario
    asignaturas = Asignaturas.objects.filter(estado='activo')
    categorias = CategoriasTemas.objects.filter(estado='activo')
    form = ConsultaForm()
    
    context = {
        'asignaturas': asignaturas,
        'categorias': categorias,
        'estudiante': estudiante,
        'form': form,
    }
    
    return render(request, 'EduConnectApp/crear_consulta.html', context)

def responder_consulta(request, consulta_id):
    """Vista para que los docentes respondan consultas"""
    if 'usuario_id' not in request.session or request.session.get('tipo_usuario') != 'docente':
        return redirect('login')
    
    usuario_id = request.session['usuario_id']
    docente = get_object_or_404(Docentes, id_usuario=usuario_id)
    consulta = get_object_or_404(Consultas, id_consulta=consulta_id)
    
    if request.method == 'POST':
        form = RespuestaForm(request.POST, request.FILES)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.id_consulta = consulta
            respuesta.id_docente = docente
            respuesta.fecha_respuesta = timezone.now()

            # calcular tiempo de respuesta de forma segura
            try:
                if consulta.fecha_consulta:
                    fc = consulta.fecha_consulta
                    # make aware if stored as naive datetime
                    try:
                        from django.utils import timezone as djtz
                        if timezone.is_naive(fc):
                            fc = timezone.make_aware(fc, timezone.get_default_timezone())
                    except Exception:
                        # if anything goes wrong with timezone conversion, fall back
                        logger.debug('responder_consulta: unable to coerce consulta.fecha_consulta to aware; proceeding without conversion')

                    tiempo_respuesta = timezone.now() - fc
                    respuesta.tiempo_respuesta_horas = int(tiempo_respuesta.total_seconds() / 3600)
                else:
                    # fecha_consulta missing in DB; leave tiempo_respuesta_horas null
                    respuesta.tiempo_respuesta_horas = None
            except Exception:
                logger.exception('responder_consulta: error computing tiempo_respuesta')
                respuesta.tiempo_respuesta_horas = None

            # Guardar archivo adjunto de forma segura
            if request.FILES.get('adjunto_archivo'):
                try:
                    file = request.FILES['adjunto_archivo']
                    path = default_storage.save(f"adjuntos/{file.name}", ContentFile(file.read()))
                    respuesta.adjunto_archivo = path
                except Exception:
                    logger.exception('responder_consulta: error saving uploaded file')
                    messages.error(request, 'Error al guardar archivo adjunto')

            # Guardar respuesta y actualizar estado de la consulta
            try:
                respuesta.save()
                consulta.estado = 'respondida'
                consulta.save()
                messages.success(request, 'Respuesta enviada exitosamente')
                return redirect('dashboard_docente')
            except Exception:
                logger.exception('responder_consulta: error saving respuesta or updating consulta')
                messages.error(request, 'Ocurrió un error al guardar la respuesta. Inténtalo de nuevo más tarde')
                return redirect('dashboard_docente')
        else:
            messages.error(request, 'Corrige los errores del formulario')
    
    form = RespuestaForm()
    context = {
        'consulta': consulta,
        'docente': docente,
        'form': form,
    }
    
    return render(request, 'EduConnectApp/responder_consulta.html', context)

@csrf_protect
def editar_respuesta(request, respuesta_id):
    """Vista para que los docentes editen una respuesta existente"""
    if 'usuario_id' not in request.session or request.session.get('tipo_usuario') != 'docente':
        return redirect('login')
    
    usuario_id = request.session['usuario_id']
    docente = get_object_or_404(Docentes, id_usuario=usuario_id)
    respuesta = get_object_or_404(Respuestas, id_respuesta=respuesta_id)
    
    # Verificar que la respuesta fue enviada por este docente
    if respuesta.id_docente.id_docente != docente.id_docente:
        messages.error(request, 'No tienes permiso para editar esta respuesta')
        return redirect('dashboard_docente')
    
    if request.method == 'POST':
        form = RespuestaForm(request.POST, request.FILES, instance=respuesta)
        if form.is_valid():
            respuesta_actualizada = form.save(commit=False)
            respuesta_actualizada.updated_at = timezone.now()
            
            # Guardar nuevo archivo adjunto si se proporciona
            if request.FILES.get('adjunto_archivo'):
                try:
                    file = request.FILES['adjunto_archivo']
                    path = default_storage.save(f"adjuntos/{file.name}", ContentFile(file.read()))
                    respuesta_actualizada.adjunto_archivo = path
                except Exception as e:
                    logger.exception('editar_respuesta: error saving uploaded file')
                    messages.error(request, 'Error al guardar el archivo adjunto')
                    return render(request, 'EduConnectApp/editar_respuesta.html', {
                        'respuesta': respuesta,
                        'form': form,
                        'consulta': respuesta.id_consulta
                    })
            
            try:
                respuesta_actualizada.save()
                messages.success(request, 'Respuesta actualizada correctamente')
                return redirect('dashboard_docente')
            except Exception as e:
                logger.exception('editar_respuesta: error saving respuesta')
                messages.error(request, 'Ocurrió un error al actualizar la respuesta')
                return redirect('dashboard_docente')
        else:
            messages.error(request, 'Corrige los errores del formulario')
    else:
        form = RespuestaForm(instance=respuesta)
    
    context = {
        'respuesta': respuesta,
        'consulta': respuesta.id_consulta,
        'docente': docente,
        'form': form,
        'es_edicion': True,
    }
    
    return render(request, 'EduConnectApp/editar_respuesta.html', context)

@csrf_protect
def ver_respuesta(request, respuesta_id):
    """Vista para ver el detalle de una respuesta guardada"""
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    respuesta = get_object_or_404(Respuestas, id_respuesta=respuesta_id)
    usuario_id = request.session['usuario_id']
    
    # Verificar permisos: el docente que la escribió o un admin
    usuario = Usuarios.objects.get(id_usuario=usuario_id)
    es_autor = respuesta.id_docente.id_usuario.id_usuario == usuario_id
    es_admin = usuario.tipo_usuario == 'admin'
    es_estudiante = respuesta.id_consulta.id_estudiante.id_usuario.id_usuario == usuario_id
    
    if not (es_autor or es_admin or es_estudiante):
        messages.error(request, 'No tienes permiso para ver esta respuesta')
        return redirect('home')
    
    context = {
        'respuesta': respuesta,
        'consulta': respuesta.id_consulta,
        'es_autor': es_autor,
    }
    
    return render(request, 'EduConnectApp/ver_respuesta.html', context)

@csrf_protect
def eliminar_respuesta(request, respuesta_id):
    """Vista para eliminar una respuesta enviada"""
    if 'usuario_id' not in request.session or request.session.get('tipo_usuario') != 'docente':
        return redirect('login')
    
    usuario_id = request.session['usuario_id']
    docente = get_object_or_404(Docentes, id_usuario=usuario_id)
    respuesta = get_object_or_404(Respuestas, id_respuesta=respuesta_id)
    
    # Verificar que la respuesta fue enviada por este docente
    if respuesta.id_docente.id_docente != docente.id_docente:
        messages.error(request, 'No tienes permiso para eliminar esta respuesta')
        return redirect('dashboard_docente')
    
    if request.method == 'POST':
        # Eliminar el archivo adjunto si existe
        if respuesta.adjunto_archivo:
            try:
                default_storage.delete(respuesta.adjunto_archivo.name)
            except Exception as e:
                logger.exception('eliminar_respuesta: error deleting file')
        
        # Cambiar el estado de la consulta a "pendiente" si esta era la única respuesta
        consulta = respuesta.id_consulta
        respuesta.delete()
        
        # Actualizar estado de la consulta si es necesario
        otras_respuestas = Respuestas.objects.filter(id_consulta=consulta).count()
        if otras_respuestas == 0:
            consulta.estado = 'pendiente'
            consulta.save()
        
        messages.success(request, 'Respuesta eliminada correctamente')
        return redirect('dashboard_docente')
    
    # GET - mostrar confirmación
    context = {
        'respuesta': respuesta,
        'consulta': respuesta.id_consulta,
    }
    
    return render(request, 'EduConnectApp/confirmar_eliminar_respuesta.html', context)

def ver_consulta(request, consulta_id):
    """Vista para ver detalles de una consulta con sus respuestas"""
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    consulta = get_object_or_404(Consultas, id_consulta=consulta_id)
    respuestas = Respuestas.objects.filter(id_consulta=consulta).order_by('fecha_respuesta')
    
    context = {
        'consulta': consulta,
        'respuestas': respuestas,
    }
    
    return render(request, 'EduConnectApp/ver_consulta.html', context)


@csrf_exempt
def debug_css_report(request):
    """Temporary endpoint: accepts POST with JSON body describing computed styles
    from the client and saves it to tmp/debug_styles.json for offline inspection.
    Only for local development.
    """
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'POST required'}, status=400)
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        return JsonResponse({'ok': False, 'error': f'invalid json: {e}'}, status=400)
    try:
        with open('tmp/debug_styles.json', 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return JsonResponse({'ok': False, 'error': f'write failed: {e}'}, status=500)
    return JsonResponse({'ok': True})


@csrf_exempt
def translate_text(request):
    """
    Vista para traducir texto usando la biblioteca 'translators'.
    Recibe un POST con {'text': 'texto a traducir'}.
    Devuelve un JSON con {'translation': 'texto traducido'}.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text_to_translate = data.get('text', '')
            if not text_to_translate:
                return JsonResponse({'error': 'No text provided'}, status=400)

            # Usar la biblioteca de traducción
            import translators as ts
            translated_text = ts.translate_text(text_to_translate, to_language='es')
            
            return JsonResponse({'translation': translated_text})
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
