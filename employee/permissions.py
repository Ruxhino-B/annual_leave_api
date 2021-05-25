from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated, IsAdminUser
from roles.models import UserRole
import logging


logger = logging.getLogger(__name__)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class HrOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        try:
            user_roles = UserRole.objects.filter(user_id=request.user)
            return any(str(user_role) == "Hr_specialist" for user_role in user_roles)

        except Exception as e:
            logger.exception(e)
            logger.error('Something went wrong!')

    # def has_object_permission(self, request, view, obj):
    #     try:
    #         if request.method in SAFE_METHODS:
    #             return True
    #         else:
    #             obj.user == request.user
    #     except Exception as e:
    #         logger.exception(e)
    #         logger.error('Something went wrong!')


class ReadOnlyHimselfsOrIsHr(BasePermission):
    """User can watch only his detail, HR have all CRUD permissions, but HR user can't change detail for himself"""
    def has_object_permission(self, request, view, obj):
        try:
            if obj.user == request.user:
                # return request.method in SAFE_METHODS or HrOrReadOnly.has_permission(self, request, view)
                return request.method in SAFE_METHODS
            else:
                return HrOrReadOnly.has_permission(self, request, view)

        except Exception as e:
            logger.exception(e)
            logger.error('Something went wrong!')
