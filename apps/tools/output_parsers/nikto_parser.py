import re

def parse(raw_output: str) -> dict:
    """
    Parses Nikto output into standardized findings.
    """
    findings = []
    # Pattern for "+ OSVDB-3092: /admin/: This might be interesting..."
    pattern = re.compile(r"\+ (OSVDB-\d+: )?([^:]+): (.*)")
    
    for line in raw_output.splitlines():
        match = pattern.search(line)
        if match:
            osvdb = match.group(1).strip(": ") if match.group(1) else None
            location = match.group(2).strip()
            details = match.group(3).strip()
            
            # Simple severity heuristic
            severity = "info"
            if any(word in details.lower() for word in ["vulnerable", "exploit", "unauthenticated", "rce"]):
                severity = "high"
            elif any(word in details.lower() for word in ["interesting", "potential", "warning"]):
                severity = "medium"
            elif osvdb:
                severity = "low"

            findings.append({
                "title": f"Nikto Finding: {location}",
                "description": f"{osvdb + ': ' if osvdb else ''}{details}",
                "severity": severity,
                "location": location,
                "evidence": match.group(0)
            })
            
    return {
        "findings": findings,
        "count": len(findings)
    }
