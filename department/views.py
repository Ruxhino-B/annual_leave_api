from django.shortcuts import render
from rest_framework import generics
from .models import Department
from .serializers import DepartmentSerializers


# Create your views here.

class DepartmentSerializerListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializers

