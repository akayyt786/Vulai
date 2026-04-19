from .llm_client import LLMClient
from .prompts import CHAIN_ANALYSIS_PROMPT
from .parser import parse_llm_response
from apps.scans.models import Finding
from utils.error_logger import log_error

def analyse_chains(scan_id):
    """
    Reviews findings for a scan and identifies potential attack chains.
    Creates new Findings in the DB if chains are found.
    """
    try:
        findings = Finding.objects.filter(scan_id=scan_id, is_chained=False)
        if findings.count() < 2:
            return []
            
        # Format findings for prompt
        findings_data = [
            {"id": str(f.id), "title": f.title, "severity": f.severity, "description": f.description}
            for f in findings
        ]
        
        llm = LLMClient()
        prompt = CHAIN_ANALYSIS_PROMPT.format(findings=findings_data)
        
        raw_response = llm.call_llm("You are a security analyst.", prompt)
        response = parse_llm_response(raw_response)
        
        chains = response.get("chains", [])
        created_findings = []
        
        for chain in chains:
            # Create a new Finding record for the chain
            new_finding = Finding.objects.create(
                scan_id=scan_id,
                title=chain.get("title", "Identified Attack Chain"),
                description=chain.get("description", ""),
                severity=chain.get("severity", "high"),
                is_chained=True,
                chained_from=chain.get("findings", []),
                layer=6, # Chains are Layer 6 per spec
                surface="chain_analysis"
            )
            created_findings.append(new_finding)
            
        return created_findings

    except Exception as e:
        log_error("apps.orchestrator.chain_analyser", "ChainAnalyserError", str(e), {"scan_id": scan_id}, exc=e)
        return []
