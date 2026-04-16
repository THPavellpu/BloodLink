"""
URL configuration for bloodlink_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth endpoints
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App URLs
    path('api/', include('users.urls')),
    path('api/', include('requests.urls')),
    path('api/', include('matching.urls')),
    path('api/', include('ai_integration.urls')),
    path('api/', include('notifications.urls')),
]
