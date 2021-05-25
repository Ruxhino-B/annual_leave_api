from django.urls import path
from .views import EmployeeSerializerListView, EmployeeSerializerCreateApiView, EmployeeSerializerDetailView

urlpatterns = [
    path('<int:pk>', EmployeeSerializerDetailView.as_view(), name='emp_detail'),
    path('', EmployeeSerializerListView.as_view(), name='emp_list'),
    path('add/', EmployeeSerializerCreateApiView.as_view(), name='create_api_view')
]