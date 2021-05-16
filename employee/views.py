from django.shortcuts import render
from rest_framework import generics
from .models import Employee
from .serializers import EmployeeSerializers

# Create your views here.

class EmployeeSerializerListView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializers