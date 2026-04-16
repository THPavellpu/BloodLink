"""
URL configuration for requests app.
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BloodRequestViewSet

router = DefaultRouter()
router.register(r'request', BloodRequestViewSet, basename='request')

urlpatterns = router.urls
