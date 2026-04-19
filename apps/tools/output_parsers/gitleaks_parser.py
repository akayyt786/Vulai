import json

def parse(raw_output: str) -> dict:
    """
    Parses gitleaks JSON output into standardized findings.
    """
    findings = []
    try:
        data = json.loads(raw_output)
        if not isinstance(data, list):
            return {"findings": [], "count": 0}
            
        for d in data:
            findings.append({
                "title": f"Gitleaks: {d.get('Description', 'Secret discovered')}",
                "description": f"Rule: {d.get('RuleID')} | Commit: {d.get('Commit', 'N/A')}",
                "severity": "high",
                "location": f"{d.get('File')}:{d.get('StartLine')}",
                "evidence": f"Match: {d.get('Match', '')[:20]}..."
            })
        return {
            "findings": findings,
            "count": len(findings)
        }
    except json.JSONDecodeError:
        return {"findings": [], "count": 0, "error": "Failed to parse gitleaks JSON"}
