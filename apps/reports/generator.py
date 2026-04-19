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
        
        # 2. Get Executive Summary and Attack Narrative via LLM
        findings_data = [
            {"id": str(f.id), "title": f.title, "severity": f.severity, "location": f.location, "description": f.description}
            for f in findings
        ]
        
        narrative_prompt = f"""
        You are a senior penetration tester writing an executive report.
        Based on the following findings, provide:
        1. A 3-sentence Executive Summary highlighting the most critical risks.
        2. A 2-paragraph Attack Narrative explaining how an attacker could realistically pivot through these findings.
           If there are chains (is_chained=True), emphasize those.

        Findings:
        {findings_data}

        Respond in JSON:
        {{"summary": "...", "narrative": "..."}}
        """
        
        llm = LLMClient()
        raw_response = llm.call_llm("You are a professional security auditor.", narrative_prompt)
        parsed = parse_llm_response(raw_response)
        
        summary = parsed.get("summary", "Executive summary could not be generated.")
        narrative = parsed.get("narrative", "Attack narrative could not be generated.")

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
                "summary": summary,
                "attack_narrative": narrative,
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
