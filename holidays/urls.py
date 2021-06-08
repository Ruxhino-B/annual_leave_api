from django.urls import path
from .views import HollidaySerializerCreateView, HollidaysSerializersApiView

urlpatterns = [
    path('', HollidaysSerializersApiView.as_view()),
    path('create/', HollidaySerializerCreateView.as_view()),
]
