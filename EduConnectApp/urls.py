from django.urls import path, include
from . import views
from .api import urls as api_urls

urlpatterns = [
    # Páginas principales
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('login/docente/', views.login_docente, name='login_docente'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/estudiante/', views.dashboard_estudiante, name='dashboard_estudiante'),
    path('dashboard/docente/', views.dashboard_docente, name='dashboard_docente'),
    path('panel/docente/', views.panel_docente, name='panel_docente'),
    
    # Consultas
    path('consulta/crear/', views.crear_consulta, name='crear_consulta'),
    path('consulta/<int:consulta_id>/', views.ver_consulta, name='ver_consulta'),
    path('consulta/<int:consulta_id>/responder/', views.responder_consulta, name='responder_consulta'),
    path('respuesta/<int:respuesta_id>/ver/', views.ver_respuesta, name='ver_respuesta'),
    path('respuesta/<int:respuesta_id>/editar/', views.editar_respuesta, name='editar_respuesta'),
    path('respuesta/<int:respuesta_id>/eliminar/', views.eliminar_respuesta, name='eliminar_respuesta'),
    # API
    path('api/', include((api_urls, 'api'))),
    # Dashboard extras
    path('mis-consultas/', views.mis_consultas, name='mis_consultas'),
    path('mi-progreso/', views.mi_progreso, name='mi_progreso'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    # Temporary debug endpoint to receive computed styles from client for diagnostics
    path('debug/_css_report/', views.debug_css_report, name='debug_css_report'),
]