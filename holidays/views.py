from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Hollidays
from .serializers import HolidaysSerializer
from employee.permissions import HrOrReadOnly

# Create your views here.

class HollidaysSerializersApiView(generics.ListAPIView):
    serializer_class = HolidaysSerializer
    queryset = Hollidays.objects.all()
    permission_classes = [AllowAny]

class HollidaySerializerCreateView(generics.ListCreateAPIView):
    queryset = Hollidays.objects.all()
    serializer_class = HolidaysSerializer
    permission_classes = [HrOrReadOnly]