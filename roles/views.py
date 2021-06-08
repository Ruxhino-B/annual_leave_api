from django.shortcuts import render
from rest_framework import generics
from .models import Rolet, UserRole
from .serializers import RoleSerializers, UserRoleSerializer
from employee.permissions import HrOrReadOnly

# Create your views here.

class RoleSerializersListView(generics.ListCreateAPIView):
    queryset = Rolet.objects.all()
    serializer_class = RoleSerializers
    permission_classes = [HrOrReadOnly]

class RoleSerializerRetriveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rolet.objects.all()
    serializer_class = RoleSerializers
    permission_classes = [HrOrReadOnly]

class UserRoleSerializersListView(generics.ListCreateAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [HrOrReadOnly]

class UserRoleSerializerRetriveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [HrOrReadOnly]