import re

def parse(raw_output: str) -> dict:
    """
    Parses raw Nmap terminal output into structured findings for the LLM.
    """
    findings = []
    
    # Regex to match open ports: "80/tcp open http Apache httpd 2.4.41"
    port_pattern = re.compile(r'^(\d+)/([a-z]+)\s+open\s+([\w\-]+)\s*(.*)$', re.MULTILINE)
    
    for match in port_pattern.finditer(raw_output):
        port = match.group(1)
        protocol = match.group(2)
        service = match.group(3)
        version_info = match.group(4).strip()
        
        description = f"Service: {service}"
        if version_info:
            description += f" | Version: {version_info}"
            
        findings.append({
            "title": f"Open Port Discovered: {port}/{protocol}",
            "description": description,
            "severity": "info", # Open ports are info-level until vulnerable services are found
            "location": f"Port {port}",
            "evidence": match.group(0)
        })

    return {
        "findings": findings,
        "count": len(findings),
        "raw_summary": f"Nmap discovered {len(findings)} open ports."
    }
