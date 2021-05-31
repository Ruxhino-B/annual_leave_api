from django.shortcuts import render
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from requests import Response as rep
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import LejeSerializers, PranimRefuzimSerializers
from .models import Leje, ApprovimLeje
from roles.models import UserRole
from employee.models import Employee
from rest_framework import status
from .permissions import EmployeeHimself, ManagerOrReadOnly, HrOnly, ManagerOnly
import logging

logger = logging.getLogger(__name__)


class LejeSerializerDetailView(generics.RetrieveAPIView):
    serializer_class = LejeSerializers
    permission_classes = [ManagerOrReadOnly]
    queryset = Leje.objects.all()

    # def get_queryset(self):
    #     try:
    #         user = self.request.user
    #         emp = Employee.objects.get(user=user)
    #         return emp.employee_id.all()
    #     except TypeError:
    #         return Leje.objects.all()
    #     else:
    #         return Leje.objects.all()


class LejeSerializerCreateView(generics.CreateAPIView):
    serializer_class = LejeSerializers
    permission_classes = [IsAuthenticated]
    queryset = Leje.objects.all()

    def perform_create(self, serializer):
        serializer.save(employee_id=self.request.user.e_user)


class LejeSerializerListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LejeSerializers

    def get_queryset(self):
        user = self.request.user
        employee = user.e_user
        user_roles_is_manager = UserRole.objects.filter(user_id=user, name__contains='Manager')
        user_roles_is_hr = UserRole.objects.filter(user_id=user, name__contains='Hr')
        department = employee.department
        department_users = Employee.objects.filter(department=department)
        manager_users = UserRole.objects.filter(name__contains='Manager')
        list_manager_employee = []
        for rol in manager_users:
            list_manager_employee.append(rol.user_id.e_user)
        if bool(user_roles_is_manager):
            if user_roles_is_hr:
                return Leje.objects.filter(Q(employee_id__in=list_manager_employee) | Q(employee_id=department_users))#, Leje.objects.filter(employee_id__in=department_users)
            else:
                return Leje.objects.filter(employee_id__in=department_users)
        elif bool(user_roles_is_hr):
            return Leje.objects.filter(Q(employee_id__in=list_manager_employee) | Q(employee_id=employee))#, Leje.objects.filter(employee_id=employee)
        else:
            return Leje.objects.filter(employee_id=employee)

class PranimRefuzimCreateApiView(generics.CreateAPIView):
    permission_classes = [HrOnly | ManagerOnly]
    serializer_class = PranimRefuzimSerializers
    #queryset = ApprovimLeje.objects.all()

    def post(self, request, *args, **kwargs):
        post_data = request.data
        aprovues = self.request.user
        aprovues_department = aprovues.e_user.department

        all_user_in_same_dep_like_manager = Employee.objects.filter(department=aprovues_department)
        mydata = post_data["leje"]
        manager_role = UserRole.objects.filter(name__contains='Manager')
        manager_list_emp=[]
        for rol in manager_role:
            manager_list_emp.append(rol.user_id.e_user)
        obj_leje = Leje.objects.get(id=mydata)
        print(obj_leje)
        print(post_data['leje'])
        print(post_data['name'])
        print(post_data)
        status = {"statusi":True}
        print(status['statusi'])
        # lejet = Leje.objects.get(id=post_data['leje'])
        if obj_leje.employee_id in all_user_in_same_dep_like_manager and obj_leje.employee_id is not aprovues.e_user:
            try:
                    data_to_add = ApprovimLeje.objects.create(name=post_data['name'], koment=post_data['koment'], status=status['statusi'], leje=obj_leje, manager=aprovues)
                    data_to_add.save()

            except IntegrityError as e:
                return Response({"message": "You have Duplicate AprovimLeje"})
                logger.exception(e)
                logger.error("ka dublikim ne database")
        elif obj_leje.employee_id in manager_list_emp and aprovues_department == "HR":
            try:
                    data_to_add = ApprovimLeje.objects.create(name=post_data['name'], koment=post_data['koment'], status=status['statusi'], leje=obj_leje, manager=aprovues)
                    data_to_add.save()

            except IntegrityError as e:
                return Response({"message": "You have Duplicate AprovimLeje"})
                logger.exception(e)
                logger.error("ka dublikim ne database")
        else:
            return Response({"message":"You have no premissions"})

        #data_to_add.leje.add(obj_leje)

        serializer = PranimRefuzimSerializers(data=data_to_add)

        print({"mesage":f"{request.data['leje']} aprovues->{aprovues}"})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)




    # def create(self, request, *args, **kwargs):
    #     post_data = request.data
    #     #emp_leje = post_data['ApprovimLeje']
    #     manager = self.request.user
    #     manager_employee = manager.e_user
    #     manager_department = manager_employee.department
    #     all_employees_in_manager_departmetn = Employee.objects.filter(department=manager_department)
    #     # new_leje = Leje.objects.create(name=post_data['leje']['name'], employee_id=post_data['leje']['employee_id'], fund_leje=post_data['leje']['fund_leje'])
    #     # new_leje.save()
    #     employe_list = []
    #     new_aprovim_leje = ApprovimLeje.objects.create(name=post_data["name"], koment=post_data["koment"], status=post_data["status"].capitalize(), manager=manager)
    #     new_aprovim_leje.save()
    #     for employee in post_data['leje']:
    #         employee_obj = Leje.objects.get(id=employee)
    #         new_aprovim_leje.leje.add(employee_obj)
    #     #leje = Leje.objects.get(id=3)
    #     #if post_data['leje']['employee_id'] in all_employees_in_manager_departmetn:
    #     print(employee, employee_obj)
    #
    #     #new_aprovim_leje = ApprovimLeje.objects.create(name=post_data["name"], koment=post_data["koment"], status=post_data["status"],leje=leje, manager=manager)
    #
    #     # for leje_id in post_data['leje']:
    #     #     leje_obj = Leje.objects.get(id=2)
    #     #     new_aprovim_leje.leje.add(leje_obj)
    #     # print(leje_id, "ketu_printi")
    #
    #
    #
    #
    #     serializer = PranimRefuzimSerializers(new_aprovim_leje)
    #     return Response(serializer.data)



