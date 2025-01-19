from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission to allow access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

