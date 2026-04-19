from celery import shared_task
from apps.orchestrator.agent import OrchestratorAgent
from apps.reports.generator import generate_report
from utils.error_logger import log_error
from .models import Scan

@shared_task(bind=True, name="apps.scans.tasks.run_scan_task")
def run_scan_task(self, scan_id):
    """
    Celery task to run a penetration test scan autonomously.
    """
    try:
        agent = OrchestratorAgent(scan_id)
        agent.run_scan()
        
        # Generate final report
        generate_report(scan_id)
        
        return f"Scan {scan_id} completed successfully."
    except Exception as e:
        log_error("apps.scans.tasks", "CeleryTaskError", str(e), {"scan_id": scan_id}, exc=e)
        
        # Update scan status to failed
        try:
            scan = Scan.objects.get(id=scan_id)
            scan.status = 'failed'
            scan.save()
        except:
            pass
            
        raise e

