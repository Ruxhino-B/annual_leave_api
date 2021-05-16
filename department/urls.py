from django.urls import path
from .views import DepartmentSerializerListView

urlpatterns = [
    path('',DepartmentSerializerListView.as_view(), name='dep_lsit'),
]