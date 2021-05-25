from django.shortcuts import render
from rest_framework.response import Response
from .models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Employee
from .serializers import EmployeeSerializers
from .permissions import ReadOnly, HrOrReadOnly, ReadOnlyHimselfsOrIsHr


# Create your views here.

class EmployeeSerializerListView(generics.ListCreateAPIView):
    """Create and List element of all Employees"""
    serializer_class = EmployeeSerializers
    queryset = Employee.objects.all()
    permission_classes = [HrOrReadOnly]

    # def get_queryset(self):
    #     useri = self.request.user.id
    #     return Employee.objects.all()


class EmployeeSerializerCreateApiView(generics.CreateAPIView):
    serializer_class = EmployeeSerializers
    queryset = Employee.objects.all()
    permission_classes = [HrOrReadOnly]


class EmployeeSerializerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View Detail on Employee, Update, Delete """
    serializer_class = EmployeeSerializers

    permission_classes = [ReadOnlyHimselfsOrIsHr]
    queryset = Employee.objects.all()

    def delete(self, request, *args, **kwargs):
        emp_pk = kwargs['pk']
        emp = User.objects.get(id=emp_pk)
        emp.is_active = False
        emp.save()
        return Response({"message":f"{emp.username} is Deactivate as User {emp.is_active}"})