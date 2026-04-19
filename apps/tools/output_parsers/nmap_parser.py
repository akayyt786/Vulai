import re

def parse(raw_output: str) -> dict:
    findings = []
    pattern = re.compile(r"(\d+)/(tcp|udp)\s+open\s+(\S+)\s*(.*)")
    
    for line in raw_output.splitlines():
        match = pattern.search(line)
        if match:
            findings.append({
                "title": f"Open Port: {match.group(1)}/{match.group(2)}",
                "description": f"Service: {match.group(3)} Version: {match.group(4).strip()}",
                "severity": "info",
                "location": f"Port {match.group(1)}"
            })
            
    return {"findings": findings, "count": len(findings)}
