"""URLs de l'API REST pour l'application Trajets."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrajetViewSet

router = DefaultRouter()
router.register(r'', TrajetViewSet, basename='trajet')

app_name = 'api-trajets'
urlpatterns = [path('', include(router.urls))]
