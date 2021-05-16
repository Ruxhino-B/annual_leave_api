from django.urls import path
from .views import EmployeeSerializerListView

urlpatterns = [
    path('', EmployeeSerializerListView.as_view(), name='emp_list'),
]