import json
from apps.scans.models import Scan, ScanStep, Finding

def build_context(scan_id):
    """
    Rebuilds the complete scan context from the database.
    This dict is sent to the LLM on every step.
    """
    try:
        scan = Scan.objects.get(id=scan_id)
        steps = ScanStep.objects.filter(scan=scan).order_by('step_number')
        findings = Finding.objects.filter(scan=scan)
        
        # Summarize findings for context
        findings_summary = [
            {"id": str(f.id), "title": f.title, "severity": f.severity, "surface": f.surface}
            for f in findings
        ]
        
        # Tools run
        tools_run = list(steps.values_list('tool_name', flat=True).distinct())
        
        # Last tool output summary
        last_output = ""
        if steps.exists():
            last_step = steps.last()
            last_output = json.dumps(last_step.parsed_output)[:2000] # Limit size
            
        # Calculate remaining surfaces for this layer and type
        from .pivot_engine import ATTACK_SURFACE_MATRIX
        matrix = ATTACK_SURFACE_MATRIX.get(scan.input_type, {})
        all_surfaces = []
        for layer_surfaces in matrix.values():
            all_surfaces.extend(layer_surfaces)
        
        remaining = [s for s in all_surfaces if s not in scan.surfaces_covered]
            
        context = {
            "input_type": scan.input_type,
            "input_value": scan.input_value,
            "current_layer": scan.current_layer,
            "surfaces_covered": scan.surfaces_covered,
            "remaining_surfaces": remaining,
            "tools_run": tools_run,
            "findings_summary": findings_summary,
            "step_count": steps.count(),
            "last_tool_output_summary": last_output,
            "target": scan.input_value
        }
        
        return context
    except Scan.DoesNotExist:
        return {}
    except Exception as e:
        # Import here to avoid circular imports if needed
        from utils.error_logger import log_error
        log_error("apps.orchestrator.context_manager", "ContextBuildError", str(e), {"scan_id": scan_id}, exc=e)
        return {}
