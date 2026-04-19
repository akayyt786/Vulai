import re

def parse(raw_output: str) -> dict:
    """
    Parses nikto output for vulnerabilities.
    """
    findings = []
    # Pattern for "+ OSVDB-3092: /admin/: This might be interesting..."
    pattern = re.compile(r"\+ (OSVDB-\d+: )?(.*)")
    
    for line in raw_output.splitlines():
        match = pattern.search(line)
        if match:
            findings.append({"description": match.group(2).strip()})
            
    return {
        "findings": findings,
        "count": len(findings)
    }
