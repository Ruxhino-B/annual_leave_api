from django.shortcuts import render
import datetime
from django.db import IntegrityError
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import LejeSerializers, PranimRefuzimSerializers
from .models import Leje, ApprovimLeje
from roles.models import UserRole
from employee.models import Employee
from holidays.models import Hollidays
from rest_framework import status
from .permissions import EmployeeHimself, ManagerOrReadOnly, HrOnly, ManagerOnly
import logging

logger = logging.getLogger(__name__)
holidays_list = []
for holidays in Hollidays.objects.all():
    holidays_list.append(holidays.dita)


class LejeSerializerDetailView(generics.RetrieveAPIView):
    serializer_class = LejeSerializers
    permission_classes = [ManagerOrReadOnly]
    queryset = Leje.objects.all()


class LejeSerializerCreateView(generics.CreateAPIView):
    serializer_class = LejeSerializers
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_data = request.data
        print(request.data._mutable)
        if post_data['fillim_leje'] > str(datetime.datetime.now()) and post_data['fillim_leje'] < post_data[
            'fund_leje']:
            data_to_add = Leje.objects.create(name=post_data['name'], employee_id=self.request.user.e_user,
                                              fillim_leje=post_data['fillim_leje'], fund_leje=post_data['fund_leje'])
            data_to_add.save()

            serializer = LejeSerializers(data=data_to_add)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response({"message1": "Fillim_date must be Grater than Today",
                         "massage2": "Fillim_date must be less then End Date"})

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
                return Leje.objects.filter(Q(employee_id__in=list_manager_employee) | Q(
                    employee_id=department_users))  # , Leje.objects.filter(employee_id__in=department_users)
            else:
                return Leje.objects.filter(employee_id__in=department_users)
        elif bool(user_roles_is_hr):
            return Leje.objects.filter(Q(employee_id__in=list_manager_employee) | Q(
                employee_id=employee))  # , Leje.objects.filter(employee_id=employee)
        else:
            return Leje.objects.filter(employee_id=employee)

def convert_days(fillim_date, fund_data, day_off):
    total_date = fund_data - fillim_date
    if total_date.days > 0:
        delta = fund_data.date() - fillim_date.date()
        days_list = []
        for i in range(delta.days + 1):
            day = fillim_date.date() + datetime.timedelta(days=i)
            days_list.append(day)
        for holidays in days_list:
            if holidays.isoweekday() in range(5, 8):
                days_list.remove(holidays)
            print(holidays)
        for dit_req in days_list:
            for dit_off in day_off:
                if dit_req == dit_off:
                    days_list.remove(dit_req)
        nr_oresh = len(days_list) * 8
        return nr_oresh
    else:
        total_hours = total_date.total_seconds()/3600
        if total_hours > 8:
            total_hours = 8
        return total_hours

class PranimRefuzimCreateApiView(generics.CreateAPIView):
    permission_classes = [HrOnly | ManagerOnly]
    serializer_class = PranimRefuzimSerializers

    # queryset = ApprovimLeje.objects.all()

    def post(self, request, *args, **kwargs):
        post_data = request.data
        aprovues = self.request.user
        aprovues_department = aprovues.e_user.department
        #Ketu selektohet instanca leje.
        leje_selektuar = Leje.objects.get(id=post_data['leje'])
        employee_aplikues_per_leje = leje_selektuar.employee_id
        kohe_fillimi = leje_selektuar.fillim_leje
        kohe_perfundimi = leje_selektuar.fund_leje
        kohe_te_shfrytezuara = kohe_perfundimi - kohe_fillimi
        kohe_te_shfrytezuara_hours = convert_days(kohe_fillimi, kohe_perfundimi, holidays_list)



        all_user_in_same_dep_like_manager = Employee.objects.filter(department=aprovues_department)
        mydata = post_data["leje"]
        manager_role = UserRole.objects.filter(name__contains='Manager')
        manager_list_emp = []
        for rol in manager_role:
            manager_list_emp.append(rol.user_id.e_user)
        obj_leje = Leje.objects.get(id=mydata)

        # lejet = Leje.objects.get(id=post_data['leje'])

        if obj_leje.employee_id in all_user_in_same_dep_like_manager and obj_leje.employee_id is not aprovues.e_user:
            try:
                try:
                    employee_aplikues_per_leje.annual_days -= kohe_te_shfrytezuara_hours
                    employee_aplikues_per_leje.save()
                except ValueError as v:
                    return Response({"error-message":f"{v}"})
                data_to_add = ApprovimLeje.objects.create(name=post_data['name'], koment=post_data['koment'],
                                                          status=post_data['status'].capitalize(), leje=obj_leje,
                                                          manager=aprovues)
                data_to_add.save()

            except IntegrityError as e:
                return Response({"message": "You have Duplicate AprovimLeje"})
                logger.exception(e)
                logger.error("ka dublikim ne database")
        elif obj_leje.employee_id in manager_list_emp and aprovues_department == "HR":
            try:
                data_to_add = ApprovimLeje.objects.create(name=post_data['name'], koment=post_data['koment'],
                                                          status=status['statusi'], leje=obj_leje, manager=aprovues)
                data_to_add.save()
            except IntegrityError as e:
                return Response({"message": "You have Duplicate AprovimLeje"})
                logger.exception(e)
                logger.error("ka dublikim ne database")
        else:
            return Response({"message": "You have no premissions"})

        # data_to_add.leje.add(obj_leje)


        serializer = PranimRefuzimSerializers(data=data_to_add)


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

class PranimRefuzimApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PranimRefuzimSerializers
    def get_queryset(self):
        employee = self.request.user.e_user
        lejet = Leje.objects.filter(employee_id=employee)
        return ApprovimLeje.objects.filter(leje__in=lejet)