from django.urls import path
from .views import RoleSerializersListView, UserRoleSerializersListView, RoleSerializerRetriveDestroyView, UserRoleSerializerRetriveDestroyView

urlpatterns = [
    path('',RoleSerializersListView.as_view(),name= 'role'),
    path('<int:pk>/', RoleSerializerRetriveDestroyView.as_view()),
    path('user/', UserRoleSerializersListView.as_view(), name='user_role'),
    path('user/<int:pk>/', UserRoleSerializerRetriveDestroyView.as_view())
]