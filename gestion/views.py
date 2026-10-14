from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    Empresa, Area, TipoEquipo, EstadoOrden, Equipo, OrdenTrabajo, DetalleOrden,
)
from .serializers import (
    EmpresaSerializer, AreaSerializer, TipoEquipoSerializer,
    EstadoOrdenSerializer, EquipoSerializer, OrdenTrabajoSerializer,
    DetalleOrdenSerializer,
)
from .permissions import EsOperadorOAdmin


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet base que exige autenticación JWT y aplica permisos por rol:
    - admin_api: CRUD completo
    - operador_api: solo GET
    - sin rol: 403
    """
    permission_classes = [IsAuthenticated, EsOperadorOAdmin]


# ─── Modelos principales (CRUD completo) ─────────────────────

class EmpresaViewSet(BaseModelViewSet):
    queryset = Empresa.objects.all().order_by('id')
    serializer_class = EmpresaSerializer


class AreaViewSet(BaseModelViewSet):
    queryset = Area.objects.select_related('empresa').all().order_by('id')
    serializer_class = AreaSerializer


class EquipoViewSet(BaseModelViewSet):
    queryset = Equipo.objects.select_related('tipo_equipo', 'area').all().order_by('id')
    serializer_class = EquipoSerializer


class OrdenTrabajoViewSet(BaseModelViewSet):
    queryset = OrdenTrabajo.objects.select_related(
        'equipo', 'estado', 'propietario'
    ).all().order_by('-id')
    serializer_class = OrdenTrabajoSerializer


# ─── Modelos operacionales (solo lectura) ────────────────────

class EstadoOrdenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EstadoOrden.objects.all().order_by('id')
    serializer_class = EstadoOrdenSerializer
    permission_classes = [IsAuthenticated, EsOperadorOAdmin]


class DetalleOrdenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DetalleOrden.objects.select_related('orden').all().order_by('id')
    serializer_class = DetalleOrdenSerializer
    permission_classes = [IsAuthenticated, EsOperadorOAdmin]


# ─── Extra: TipoEquipo (opcional, no cuenta en los 6) ────────

class TipoEquipoViewSet(BaseModelViewSet):
    queryset = TipoEquipo.objects.all().order_by('id')
    serializer_class = TipoEquipoSerializer