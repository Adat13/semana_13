"""
URL configuration for convencion_project project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from convencion.views import IglesiaViewSet, ParticipanteViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Initialize DefaultRouter
router = DefaultRouter()
router.register(r'iglesias', IglesiaViewSet, basename='iglesia')
router.register(r'participantes', ParticipanteViewSet, basename='participante')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include(router.urls)),
    
    # OpenAPI Schema and Swagger UI documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
