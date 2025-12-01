from rest_framework import viewsets, permissions
from .serializers import ConsultasSerializer, RespuestasSerializer
from .serializers import ConsultasSerializer, RespuestasSerializer, UsuariosSerializer, AsignaturasSerializer, CategoriasSerializer, DocentesSerializer
from ..models import Consultas, Respuestas, Usuarios, Asignaturas, CategoriasTemas, Docentes


class ConsultasViewSet(viewsets.ModelViewSet):
    queryset = Consultas.objects.all()
    serializer_class = ConsultasSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RespuestasViewSet(viewsets.ModelViewSet):
    queryset = Respuestas.objects.all()
    serializer_class = RespuestasSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UsuariosViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AsignaturasViewSet(viewsets.ModelViewSet):
    queryset = Asignaturas.objects.all()
    serializer_class = AsignaturasSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoriasViewSet(viewsets.ModelViewSet):
    queryset = CategoriasTemas.objects.all()
    serializer_class = CategoriasSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DocentesViewSet(viewsets.ModelViewSet):
    queryset = Docentes.objects.all()
    serializer_class = DocentesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
