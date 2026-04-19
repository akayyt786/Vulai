import re

def parse(raw_output: str) -> dict:
    """
    Parses SSLyze (SSL/TLS scanner) output.
    Extracts protocol versions and heartbleed vulnerability status.
    """
    findings = []
    
    # Check for Heartbleed
    if "Heartbleed" in raw_output and "VULNERABLE" in raw_output:
        findings.append({
            "title": "Heartbleed Detected",
            "description": "The server is vulnerable to the Heartbleed (CVE-2014-0160) attack, allowing for memory disclosure.",
            "severity": "critical",
            "location": "SSL/TLS Layer",
            "evidence": "VULNERABLE string found in SSLyze output"
        })
        
    # Check for Weak Protocols
    weak_protocols = {
        "SSL 2.0": "medium",
        "SSL 3.0": "medium",
        "TLS 1.0": "low",
        "TLS 1.1": "low"
    }
    
    for proto, severity in weak_protocols.items():
        if proto in raw_output and "Accepted" in raw_output:
            findings.append({
                "title": f"Weak Protocol Enabled: {proto}",
                "description": f"The server accepts connections using outdated and weak {proto} protocol.",
                "severity": severity,
                "location": f"SSL/TLS: {proto}",
                "evidence": f"{proto}: Accepted"
            })
            
    # Check for Certificate Issues
    if "Hostname validation: FAILED" in raw_output:
        findings.append({
            "title": "SSL Hostname Mismatch",
            "description": "The certificate presented by the server does not match the requested hostname.",
            "severity": "low",
            "location": "Certificate Validation",
            "evidence": "Hostname validation: FAILED"
        })

    return {
        "status": "success",
        "findings": findings,
        "count": len(findings),
        "summary": f"SSL/TLS analysis complete, found {len(findings)} issues"
    }
