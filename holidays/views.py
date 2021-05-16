from django.shortcuts import render
from rest_framework import generics
from .models import Hollidays

# Create your views here.

class HollidaysSerializersListView(generics.GenericAPIView):
    queryset = Hollidays.objects.all()