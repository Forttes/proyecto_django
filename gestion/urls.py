from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    EmpresaViewSet, AreaViewSet, EquipoViewSet, OrdenTrabajoViewSet,
    EstadoOrdenViewSet, DetalleOrdenViewSet, TipoEquipoViewSet,
)

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'areas', AreaViewSet, basename='area')
router.register(r'equipos', EquipoViewSet, basename='equipo')
router.register(r'ordenes', OrdenTrabajoViewSet, basename='ordentrabajo')
router.register(r'estados-orden', EstadoOrdenViewSet, basename='estadoorden')
router.register(r'detalles-orden', DetalleOrdenViewSet, basename='detalleorden')
router.register(r'tipos-equipo', TipoEquipoViewSet, basename='tipoequipo')

urlpatterns = [
    path('', include(router.urls)),
]