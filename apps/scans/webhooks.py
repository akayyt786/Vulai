from rest_framework import views, status, permissions
from rest_framework.response import Response
from .serializers import ScanCreateSerializer
from .tasks import run_scan_task
import secrets

class ExternalScanWebhookView(views.APIView):
    """
    Endpoint for external triggers (n8n, GitHub, etc.)
    Example Payload: {"target": "http://example.com", "api_key": "..."}
    """
    permission_classes = [permissions.AllowAny] # In Phase 2 we use simple API key auth

    def post(self, request):
        api_key = request.data.get('api_key')
        target = request.data.get('target')
        
        # Shared Secret Auth from settings/env
        from django.conf import settings
        EXPECTED_KEY = getattr(settings, 'WEBHOOK_API_KEY', "vulnai_secret_default_key")
        
        if api_key != EXPECTED_KEY:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
            
        if not target:
            return Response({"error": "Target is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Basic validation: ensure it looks like a URL if input_type is url
        if not target.startswith(('http://', 'https://')):
             return Response({"error": "Target must be a valid URL (starting with http/https)"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the scan (input_type="url", input_value=target)
        from .models import Scan
        scan = Scan.objects.create(
            input_type='url',
            input_value=target,
            status='pending',
            consent_confirmed=True
        )
        
        run_scan_task.delay(str(scan.id))
        
        return Response({
            "status": "triggered",
            "scan_id": str(scan.id),
            "link": f"/api/scans/{scan.id}/"
        }, status=status.HTTP_201_CREATED)
