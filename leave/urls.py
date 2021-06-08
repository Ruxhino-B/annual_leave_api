from django.urls import path, include
from .views import LejeSerializerDetailView, LejeSerializerListView, LejeSerializerCreateView, PranimRefuzimCreateApiView, PranimRefuzimApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", PranimRefuzimCreateApiView, basename="pranim")

urlpatterns = [
    path('<int:pk>', LejeSerializerDetailView.as_view()),
    path('create/', LejeSerializerCreateView.as_view()),
    path('', LejeSerializerListView.as_view()),
    path('pranim', PranimRefuzimCreateApiView.as_view()),
    path('status', PranimRefuzimApiView.as_view()),
    #path('pranim', include(router.urls))
]