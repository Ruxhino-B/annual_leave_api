from django.shortcuts import render
from rest_framework import generics
from .models import Rolet, UserRole
from .serializers import RoleSerializers, UserRoleSerializer

# Create your views here.

class RoleSerializersListView(generics.ListCreateAPIView):
    queryset = Rolet.objects.all()
    serializer_class = RoleSerializers

class UserRoleSerializersListView(generics.ListCreateAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer