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
            
            # Dispatch scan
            if settings.REDIS_URL:
                run_scan_task.delay(str(scan.id))
            else:
                # Fallback for local dev without Redis: run in separate thread
                # This prevents the HTTP worker from blocking while the LLM runs
                import threading
                thread = threading.Thread(target=run_scan_task, args=(str(scan.id),))
                thread.daemon = True
                thread.start()
            
            return Response(
                {"scan_id": str(scan.id), "status": scan.status},
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            # log_error is a custom utility, we should use standard exceptions for check
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

    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        scan = self.get_object()
        if scan.status != 'running':
            return Response({"error": "Only running scans can be paused"}, status=status.HTTP_400_BAD_REQUEST)
        scan.status = 'paused'
        scan.save()
        return Response({"status": "paused"})

    @action(detail=True, methods=['post'])
    def resume(self, request, pk=None):
        scan = self.get_object()
        if scan.status == 'running':
            return Response({"status": "running"})
        if scan.status != 'paused':
            return Response({"error": f"Cannot resume scan in status: {scan.status}"}, status=status.HTTP_400_BAD_REQUEST)
        
        scan.status = 'running'
        scan.save()
        
        # Dispatch scan task to pick up from where it left off
        if settings.REDIS_URL:
            run_scan_task.delay(str(scan.id))
        else:
            import threading
            thread = threading.Thread(target=run_scan_task, args=(str(scan.id),))
            thread.daemon = True
            thread.start()
            
        return Response({"status": "running"})

    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        scan = self.get_object()
        if scan.status not in ['running', 'paused']:
            return Response({"error": "Only running or paused scans can be stopped"}, status=status.HTTP_400_BAD_REQUEST)
        scan.status = 'failed' # Or 'stopped' if we add it, but 'failed' is fine for abort
        scan.save()
        return Response({"status": "stopped"})

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
