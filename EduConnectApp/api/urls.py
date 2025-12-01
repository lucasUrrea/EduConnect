from rest_framework import routers
from .views import ConsultasViewSet, RespuestasViewSet, UsuariosViewSet, AsignaturasViewSet, CategoriasViewSet, DocentesViewSet

router = routers.DefaultRouter()
router.register(r'consultas', ConsultasViewSet)
router.register(r'respuestas', RespuestasViewSet)
router.register(r'usuarios', UsuariosViewSet)
router.register(r'asignaturas', AsignaturasViewSet)
router.register(r'categorias', CategoriasViewSet)
router.register(r'docentes', DocentesViewSet)

urlpatterns = router.urls
