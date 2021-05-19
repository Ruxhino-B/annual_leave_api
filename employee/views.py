from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Employee
from .serializers import EmployeeSerializers
from .permissions import ReadOnly, HrOrReadOnly

# Create your views here.

class EmployeeSerializerListView(generics.ListCreateAPIView):
    serializer_class = EmployeeSerializers
    queryset = Employee.objects.all()
    permission_classes = [HrOrReadOnly]


    # def get_queryset(self):
    #     useri = self.request.user.id
    #     return Employee.objects.all()

class EmployeeSerializerDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = EmployeeSerializers
    permission_classes = [HrOrReadOnly]
    queryset = Employee.objects.all()