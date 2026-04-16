"""
URL configuration for AI integration app.
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AIIntegrationViewSet

router = DefaultRouter()
router.register(r'ai', AIIntegrationViewSet, basename='ai')

urlpatterns = router.urls
