from apps.scans.models import Scan, Finding, Report
from utils.cvss_scorer import calculate_risk_score
from apps.orchestrator.llm_client import LLMClient
from apps.orchestrator.parser import parse_llm_response
from utils.error_logger import log_error

def generate_report(scan_id):
    """
    Generates the final summary report for a scan.
    """
    try:
        scan = Scan.objects.get(id=scan_id)
        findings = Finding.objects.filter(scan=scan)
        
        # 1. Calculate risk score
        risk_score = calculate_risk_score(findings)
        
        # 2. Get Executive Summary via LLM
        findings_data = [
            {"title": f.title, "severity": f.severity, "surface": f.surface}
            for f in findings
        ]
        
        llm = LLMClient()
        prompt = f"Generate a 3-5 sentence executive summary of these security findings: {findings_data}"
        raw_summary = llm.call_llm("You are a senior security auditor.", prompt)
        
        # 3. Findings count
        counts = {
            "critical": findings.filter(severity='critical').count(),
            "high": findings.filter(severity='high').count(),
            "medium": findings.filter(severity='medium').count(),
            "low": findings.filter(severity='low').count(),
            "info": findings.filter(severity='info').count(),
        }
        
        # 4. Create or update report
        report, created = Report.objects.update_or_create(
            scan=scan,
            defaults={
                "summary": raw_summary,
                "attack_narrative": "Attack chains were identified and described in individual findings.",
                "findings_count": counts,
                "surfaces_tested": scan.surfaces_covered,
                "risk_score": risk_score,
                "raw_json": {"findings": findings_data}
            }
        )
        
        return report

    except Exception as e:
        log_error("apps.reports.generator", "ReportGenerationError", str(e), {"scan_id": scan_id}, exc=e)
        return None
