from rest_framework.permissions import BasePermission, SAFE_METHODS


class EsAdminAPI(BasePermission):
    """Permite acceso solo a usuarios del grupo 'admin_api'."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name='admin_api').exists()
        )


class EsOperadorOAdmin(BasePermission):
    """
    - Admin API: acceso total (GET, POST, PUT, PATCH, DELETE).
    - Operador API: solo métodos seguros (GET, HEAD, OPTIONS).
    - Sin rol: sin acceso.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        es_admin = request.user.groups.filter(name='admin_api').exists()
        es_operador = request.user.groups.filter(name='operador_api').exists()

        if es_admin:
            return True
        if es_operador and request.method in SAFE_METHODS:
            return True
        return False


class EsAdminOOOperadorLectura(BasePermission):
    """
    Variante por si quieres usarla en un ViewSet que acepte lectura para operador.
    (Misma lógica que EsOperadorOAdmin, se deja por claridad de nombres.)
    """
    def has_permission(self, request, view):
        return EsOperadorOAdmin().has_permission(request, view)