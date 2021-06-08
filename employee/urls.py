from django.urls import path
from .views import EmployeeSerializerListView, EmployeeSerializerCreateApiView, \
    EmployeeSerializerDetailView, EmployeeSerializerDetailViewHimself, \
    EmployeeSerializerUpdateDeleteRetrive

urlpatterns = [
    path('<int:pk>', EmployeeSerializerDetailView.as_view(), name='emp_detail'),
    path('', EmployeeSerializerListView.as_view(), name='emp_list'),
    path('add/', EmployeeSerializerCreateApiView.as_view(), name='create_api_view'),
    path('profile/', EmployeeSerializerDetailViewHimself.as_view()),
    path('update/<int:pk>/', EmployeeSerializerUpdateDeleteRetrive.as_view())
]