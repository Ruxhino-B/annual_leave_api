from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Department
from .serializers import DepartmentSerializers
from employee.permissions import HrOrReadOnly


# Create your views here.

class DepartmentSerializerListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializers

class DepartmentSerializerCreateView(generics.CreateAPIView):
    serializer_class = DepartmentSerializers
    permission_classes = [IsAdminUser]

class DepartmentSerializerDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = DepartmentSerializers
    queryset = Department.objects.all()

# class DepartmentSerializerHyperLinkView(generics.ListCreateAPIView):
#     permission_classes = [IsAdminUser]
#     serializer_class = DepartmentSerializerHyperlink
#     queryset = Department.objects.all()



