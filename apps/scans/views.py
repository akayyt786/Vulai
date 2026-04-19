from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_ some
from .models import Scan, Report
from .serializers import ScanCreateSerializer, ScanStatusSerializer, ScanDetailSerializer
from apps.reports.serializers import ReportSerializer

# Celery task import
from .tasks import run_scan_task

class ScanViewSet(viewsets.ModelViewSet):
    queryset = Scan.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ScanCreateSerializer
        elif self.action == 'retrieve' or self.action == 'status':
            return ScanStatusSerializer
        return ScanDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check concurrent scans
        from django.conf import settings
        running_scans = Scan.objects.filter(status='running').count()
        if running_scans >= settings.MAX_CONCURRENT_SCANS:
            return Response(
                {"error": f"Maximum concurrent scans ({settings.MAX_CONCURRENT_SCANS}) reached."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
            
        scan = serializer.save()
        
        # Dispatch Celery task
        run_scan_task.delay(str(scan.id))
        
        return Response(
            {"scan_id": str(scan.id), "status": scan.status},
            status=status.HTTP_202_ACCEPTED
        )

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        scan = self.get_object()
        serializer = ScanStatusSerializer(scan)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        scan = self.get_object()
        try:
            report = scan.report
            serializer = ReportSerializer(report)
            return Response(serializer.data)
        except Report.DoesNotExist:
            return Response(
                {"error": "Report not generated yet or scan failed."},
                status=status.HTTP_404_NOT_FOUND
            )

class HealthCheckView(views.APIView):
    def get(self, request):
        # Basic health check - this will be expanded in Phase 8
        return Response({
            "status": "ok",
            "db": "ok",
            "celery": "not_checked" # Placeholder
        })
