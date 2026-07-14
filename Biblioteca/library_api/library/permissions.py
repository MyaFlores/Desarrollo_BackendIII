from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """Permite acceso solo a usuarios con rol ADMIN"""
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and
            request.user.profile.role == 'ADMIN'
        )

class IsBibliotecario(BasePermission):
    """Permite acceso solo a usuarios con rol BIBLIOTECARIO"""
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and
            request.user.profile.role == 'BIBLIOTECARIO'
        )

class IsAdminOrBibliotecario(BasePermission):
    """Permite acceso a ADMIN y BIBLIOTECARIO"""
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and
            request.user.profile.role in ['ADMIN', 'BIBLIOTECARIO']
        )

class IsClient(BasePermission):
    """Permite acceso solo a CLIENTE"""
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and
            request.user.profile.role == 'CLIENTE'
        )

class IsAdminOrReadOnly(BasePermission):
    """Permiso combinado: GET para todos, escritura solo ADMIN"""
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user and request.user.is_authenticated
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and
            request.user.profile.role == 'ADMIN'
        )