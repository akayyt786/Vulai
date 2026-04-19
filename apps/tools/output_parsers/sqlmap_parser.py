import re

def parse(raw_output: str) -> dict:
    """
    Parses sqlmap output for injectable parameters.
    """
    findings = []
    if "is vulnerable" in raw_output or "injectable" in raw_output:
        # Extract parameter name if possible
        param_match = re.search(r"GET parameter '(\w+)' is vulnerable", raw_output)
        if param_match:
            findings.append({"parameter": param_match.group(1), "type": "SQLi"})
            
    return {
        "findings": findings,
        "count": len(findings),
        "vulnerable": len(findings) > 0
    }
