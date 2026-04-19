import re

def parse(raw_output: str) -> dict:
    """
    Parses Dalfox (XSS scanner) output.
    Looks for verified [V] findings and proof-of-concept payloads.
    """
    findings = []
    # Pattern for "[V][GET] http://target.com/xss.php?q=xxxx ... proof: <script>..."
    # Also handle [POC] and [I] info lines
    vuln_pattern = re.compile(r"\[(V|POC|I)\]\[(\w+)\]\s+([^\s]+)\s+.*proof:\s+(.*)")
    
    for line in raw_output.splitlines():
        match = vuln_pattern.search(line)
        if match:
            tag = match.group(1)
            method = match.group(2)
            url = match.group(3)
            payload = match.group(4)
            
            severity = "high" if tag == "V" else "medium" if tag == "POC" else "info"
            title = f"Verified XSS ({method})" if tag == "V" else f"XSS PoC Detected ({method})" if tag == "POC" else f"XSS Info ({method})"
            
            findings.append({
                "title": title,
                "description": f"Dalfox detected a {title} on {url} using payload: {payload}",
                "severity": severity,
                "location": url,
                "evidence": line
            })
            
    return {
        "status": "success",
        "findings": findings,
        "count": len(findings),
        "summary": f"Detected {len(findings)} XSS related findings"
    }
