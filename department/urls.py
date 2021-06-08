from django.urls import path
from .views import DepartmentSerializerListView, DepartmentSerializerCreateView, \
    DepartmentSerializerDetailView

urlpatterns = [
    path('',DepartmentSerializerListView.as_view(), name='dep_lsit'),
    path('create/', DepartmentSerializerCreateView.as_view()),
    path('<int:pk>', DepartmentSerializerDetailView.as_view()),
   # path('dep/', DepartmentSerializerHyperLinkView.as_view()),
]