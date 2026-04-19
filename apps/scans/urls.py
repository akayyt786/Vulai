from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScanViewSet, HealthCheckView
from .webhooks import ExternalScanWebhookView

router = DefaultRouter()
router.register(r'scans', ScanViewSet, basename='scan')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', HealthCheckView.as_view(), name='health'),
    path('trigger/', ExternalScanWebhookView.as_view(), name='webhook_trigger'),
]
