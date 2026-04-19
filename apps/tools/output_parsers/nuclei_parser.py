import json

def parse(raw_output: str) -> dict:
    """
    Parses nuclei JSON output into standardized findings.
    """
    findings = []
    for line in raw_output.splitlines():
        if not line.strip(): continue
        try:
            data = json.loads(line)
            info = data.get("info", {})
            
            # Map nuclei severity to our standard scale
            severity_map = {
                "critical": "critical",
                "high": "high",
                "medium": "medium",
                "low": "low",
                "info": "info"
            }
            raw_severity = info.get("severity", "info").lower()
            severity = severity_map.get(raw_severity, "info")

            findings.append({
                "title": f"Nuclei: {data.get('template-id')}",
                "description": info.get("description", info.get("name", "Vulnerability detected")),
                "severity": severity,
                "location": data.get("matched-at") or data.get("host", ""),
                "evidence": f"Template: {data.get('template-id')} | Type: {data.get('type')}"
            })
        except json.JSONDecodeError:
            continue
            
    return {
        "findings": findings,
        "count": len(findings)
    }
