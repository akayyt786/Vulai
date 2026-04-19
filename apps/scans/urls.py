from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScanViewSet, HealthCheckView

router = DefaultRouter()
router.register(r'scans', ScanViewSet, basename='scan')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', HealthCheckView.as_view(), name='health'),
]
