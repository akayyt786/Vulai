import json

def parse(raw_output: str) -> dict:
    """
    Parses ffuf JSON output into standardized findings.
    """
    findings = []
    try:
        data = json.loads(raw_output)
        results = data.get("results", [])
        
        for r in results:
            url = r.get("url", "")
            status_code = r.get("status", 0)
            
            # Severity mapping for sensitive paths
            severity = "info"
            sensitive_keywords = ["admin", "config", "debug", "env", "backup", "db", "sql", "git", "svn", "root"]
            if any(kw in url.lower() for kw in sensitive_keywords):
                severity = "medium"
            if status_code in [200, 204, 301, 302, 307]:
                if any(kw in url.lower() for kw in [".env", "config.json", "id_rsa", "passwd"]):
                    severity = "high"

            findings.append({
                "title": f"Path Discovered: {url}",
                "description": f"Encountered HTTP {status_code} at {url}",
                "severity": severity,
                "location": url,
                "evidence": f"Status: {status_code} | Size: {r.get('length')} | Words: {r.get('words')}"
            })
            
        return {
            "findings": findings,
            "count": len(findings)
        }
    except json.JSONDecodeError:
        # Fallback for non-JSON output (e.g. error messages)
        return {
            "findings": [],
            "count": 0,
            "error": "Failed to parse ffuf JSON"
        }
