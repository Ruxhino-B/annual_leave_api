from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from roles.models import UserRole
from employee.models import Employee
import logging

logger = logging.getLogger(__name__)


class EmployeeHimself(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            if obj.employee_id.user == request.user:
                return request.method in SAFE_METHODS
        except Exception as e:
            logger.exception(e)
            logger.error('Something went wrong!')


class ManagerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            user_roles = UserRole.objects.filter(user_id=request.user, name__contains='Manager')
            department = request.user.e_user.department == obj.employee_id.department
            if user_roles and department:
                return True
            else:
                return EmployeeHimself.has_object_permission(self, request, view, obj)

        except Exception as e:
            logger.exception(e)
            logger.error('Something went wrong!')

class HrOnly(BasePermission):
    def has_permission(self, request, view):
        try:
            user_roles = UserRole.objects.filter(user_id=request.user, name__contains='Hr')
            return bool(user_roles)
        except Exception as e:
            logger.exception(e)
            logger.error('Something went wrong!')

class ManagerOnly(BasePermission):
    def has_permission(self, request, view):
        try:
            user_roles = UserRole.objects.filter(user_id=request.user, name__contains='Manager')
            return bool(user_roles)
        except Exception as e:
            logger.exception(e)
            logger.error('Something went Wrong!')
    # def has_object_permission(self, request, view, obj):
    #     try:
    #         user = request.user
    #         manager_emp = Employee.objects.get(user_id=user)
    #         manager_department = manager_emp.department
    #         all_user_in_same_department = Employee.objects.filter(department=manager_department)
    #         if obj.employee_id in all_user_in_same_department:
    #             return True
    #     except Exception as e:
    #         logger.exception(e)
    #         logger.error('Something went Wrong!')
