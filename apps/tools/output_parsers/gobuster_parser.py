import re

def parse(raw_output: str) -> dict:
    """
    Parses Gobuster (directory buster) output.
    Looks for (Status: 200), (Status: 301), etc.
    """
    findings = []
    # Pattern for "/admin (Status: 200) [Size: 512]"
    pattern = re.compile(r"(/[^\s]+)\s+\(Status:\s+(\d+)\)\s+\[Size:\s+(\d+)\]")
    
    sensitive_keywords = ['admin', 'config', 'setup', 'backup', 'env', 'git', 'sql', 'db']
    
    for line in raw_output.splitlines():
        match = pattern.search(line)
        if match:
            path = match.group(1)
            status_code = int(match.group(2))
            size = int(match.group(3))
            
            severity = "info"
            title = f"Discovered Path: {path}"
            
            if status_code == 200:
                severity = "medium"
                if any(kw in path.lower() for kw in sensitive_keywords):
                    severity = "high"
                    title = f"Sensitive Path Discovered: {path}"
            elif status_code in [301, 302, 307]:
                severity = "info"
                
            findings.append({
                "title": title,
                "description": f"Accessible path found with status {status_code} and size {size} bytes.",
                "severity": severity,
                "location": path,
                "evidence": line
            })
            
    return {
        "status": "success",
        "findings": findings,
        "count": len(findings),
        "summary": f"Discovered {len(findings)} accessible paths"
    }
