"""
URL configuration for matching app.
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DonorMatchingViewSet

router = DefaultRouter()
router.register(r'donors', DonorMatchingViewSet, basename='donors')

urlpatterns = router.urls
