"""
URLs de l'API REST pour l'application Bus.
Utilise le DefaultRouter de DRF pour générer automatiquement les URLs du ViewSet.
Préfixe : /api/bus/
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusViewSet

# Le router génère automatiquement toutes les URLs CRUD
router = DefaultRouter()
router.register(r'', BusViewSet, basename='bus')

app_name = 'api-bus'

urlpatterns = [
    path('', include(router.urls)),
]
