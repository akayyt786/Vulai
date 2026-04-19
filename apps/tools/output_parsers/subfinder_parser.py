def parse(raw_output: str) -> dict:
    """
    Parses subfinder output into standardized findings.
    """
    findings = []
    subdomains = list(set(raw_output.splitlines())) # Deduplicate
    
    for sub in subdomains:
        if not sub.strip(): continue
        findings.append({
            "title": f"Subdomain Discovered: {sub}",
            "description": f"New potential attack surface identified: {sub}",
            "severity": "info",
            "location": sub,
            "evidence": f"Discovered via subfinder reconnaissance"
        })
        
    return {
        "findings": findings,
        "count": len(findings)
    }
