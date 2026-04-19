import json

def parse(raw_output: str) -> dict:
    """
    Parses trivy JSON output into standardized findings.
    """
    findings = []
    try:
        data = json.loads(raw_output)
        results = data.get("Results", [])
        
        # Severity mapping
        severity_map = {
            "CRITICAL": "critical",
            "HIGH": "high",
            "MEDIUM": "medium",
            "LOW": "low"
        }

        for res in results:
            target = res.get("Target", "Unknown")
            vulnerabilities = res.get("Vulnerabilities", [])
            for v in vulnerabilities:
                vuln_id = v.get("VulnerabilityID")
                pkg_name = v.get("PkgName")
                title = v.get("Title", "Vulnerability detected")
                raw_severity = v.get("Severity", "info").upper()
                
                findings.append({
                    "title": f"Trivy: {vuln_id} ({pkg_name})",
                    "description": f"{title}. Installed version: {v.get('InstalledVersion')}. Fixed in: {v.get('FixedVersion', 'N/A')}",
                    "severity": severity_map.get(raw_severity, "info"),
                    "location": target,
                    "evidence": f"Vulnerability {vuln_id} found in {pkg_name}"
                })
        return {
            "findings": findings,
            "count": len(findings)
        }
    except json.JSONDecodeError:
        return {"findings": [], "count": 0, "error": "Failed to parse trivy JSON"}
