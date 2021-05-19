from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from roles.models import UserRole

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class HrOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        id_user = request.user.id
        if UserRole.objects.get(user_id=id_user) == UserRole.objects.get(name='Hr_specialit'):
            return True
        else:
            return request.method in SAFE_METHODS


