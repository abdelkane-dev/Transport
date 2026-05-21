"""URLs de l'API REST pour l'application Réservations."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationViewSet

router = DefaultRouter()
router.register(r'', ReservationViewSet, basename='reservation')

app_name = 'api-reservations'
urlpatterns = [path('', include(router.urls))]
