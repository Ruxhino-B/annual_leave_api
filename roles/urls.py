from django.urls import path
from .views import RoleSerializersListView, UserRoleSerializersListView

urlpatterns = [
    path('',RoleSerializersListView.as_view(),name= 'role'),
    path('roleuser/', UserRoleSerializersListView.as_view(), name='user_role')
]