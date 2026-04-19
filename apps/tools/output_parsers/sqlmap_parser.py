import re

def parse(raw_output: str) -> dict:
    """
    Parses sqlmap output for injectable parameters into standardized findings.
    """
    findings = []
    
    # Pattern to match injectable parameters: "GET parameter 'id' is vulnerable"
    # and vulnerable types: "Title: MySQL >= 5.0.12 combined queries ..."
    param_pattern = re.compile(r"(GET|POST|PUT|DELETE) parameter '(\w+)' is vulnerable", re.IGNORECASE)
    type_pattern = re.compile(r"Type: (.*)")
    title_pattern = re.compile(r"Title: (.*)")

    params = param_pattern.findall(raw_output)
    types = type_pattern.findall(raw_output)
    titles = title_pattern.findall(raw_output)

    for i, (method, param) in enumerate(params):
        vuln_type = types[i] if i < len(types) else "SQL Injection"
        vuln_title = titles[i] if i < len(titles) else "Injectable Parameter"
        
        findings.append({
            "title": f"SQL Injection: {method} parameter '{param}'",
            "description": f"Target is vulnerable to {vuln_type}. Payload Detail: {vuln_title}",
            "severity": "high", # Usually high, could be critical if DB info leak is easy
            "location": f"{method} {param}",
            "evidence": f"Parameter '{param}' confirmed injectable via SQLmap"
        })
            
    return {
        "findings": findings,
        "count": len(findings)
    }
