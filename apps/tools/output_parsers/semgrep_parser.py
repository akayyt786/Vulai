import json

def parse(raw_output: str) -> dict:
    """
    Parses semgrep JSON output into standardized findings.
    """
    findings = []
    try:
        data = json.loads(raw_output)
        results = data.get("results", [])
        
        # Severity mapping
        severity_map = {
            "error": "high",
            "warning": "medium",
            "info": "info"
        }

        for res in results:
            check_id = res.get("check_id")
            path = res.get("path")
            line = res.get("start", {}).get("line", 0)
            extra = res.get("extra", {})
            message = extra.get("message", "Security issue detected")
            raw_severity = extra.get("severity", "info").lower()
            
            findings.append({
                "title": f"Semgrep: {check_id}",
                "description": message,
                "severity": severity_map.get(raw_severity, "info"),
                "location": f"{path}:{line}",
                "evidence": "\n".join(extra.get("lines", "").splitlines()[:3]) # First 3 lines
            })

        return {
            "findings": findings,
            "count": len(findings)
        }
    except json.JSONDecodeError:
        return {
            "findings": [],
            "count": 0,
            "error": "Failed to parse semgrep JSON"
        }
