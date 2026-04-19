from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import connection
from django.conf import settings
from utils.error_logger import log_error
from .models import Scan, Report
from .serializers import ScanCreateSerializer, ScanStatusSerializer, ScanDetailSerializer
from apps.reports.serializers import ReportSerializer

# Celery task import
from .tasks import run_scan_task

class ScanViewSet(viewsets.ModelViewSet):
    queryset = Scan.objects.all().order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ScanCreateSerializer
        elif self.action in ['retrieve', 'status', 'list']:
            return ScanStatusSerializer
        return ScanDetailSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer_class()(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Check concurrent scans
            running_scans = Scan.objects.filter(status='running').count()
            if running_scans >= settings.MAX_CONCURRENT_SCANS:
                log_error("apps.scans.views", "ConcurrentScanLimitReached", f"Limit: {settings.MAX_CONCURRENT_SCANS}")
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
        except Exception as e:
            if not isinstance(e, (status.HTTP_400_BAD_REQUEST, status.HTTP_429_TOO_MANY_REQUESTS)):
                log_error("apps.scans.views", "ScanCreationError", str(e), request.data, exc=e)
            raise e

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        scan = self.get_object()
        serializer = ScanStatusSerializer(scan)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        scan = self.get_object()
        try:
            report = getattr(scan, 'report', None)
            if not report:
                raise Report.DoesNotExist
            serializer = ReportSerializer(report)
            return Response(serializer.data)
        except Report.DoesNotExist:
            return Response(
                {"error": "Report not generated yet or scan failed."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            log_error("apps.scans.views", "ReportFetchError", str(e), {"scan_id": pk}, exc=e)
            return Response({"error": "Internal server error fetching report"}, status=500)

class HealthCheckView(views.APIView):
    def get(self, request):
        health = {
            "status": "ok",
            "db": "ok",
            "celery": "ok"
        }
        
        # 1. DB Check
        try:
            connection.ensure_connection()
        except Exception:
            health["db"] = "failed"
            health["status"] = "degraded"
            
        # 2. Celery Check
        try:
            from config.celery import app
            ping = app.control.ping(timeout=0.5)
            if not ping:
                health["celery"] = "unavailable"
                health["status"] = "degraded"
        except Exception:
            health["celery"] = "failed"
            health["status"] = "degraded"
            
        return Response(health)
