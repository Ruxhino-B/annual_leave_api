from django.urls import path
from .views import EmployeeSerializerListView, EmployeeSerializerDetailView

urlpatterns = [
    path('<int:pk>', EmployeeSerializerDetailView.as_view(), name='emp_detail'),
    path('', EmployeeSerializerListView.as_view(), name='emp_list'),
]