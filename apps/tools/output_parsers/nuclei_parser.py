import json

def parse(raw_output: str) -> dict:
    """
    Parses nuclei output (assumes JSON format).
    """
    findings = []
    for line in raw_output.splitlines():
        try:
            data = json.loads(line)
            findings.append({
                "template_id": data.get("template-id"),
                "info": data.get("info", {}),
                "type": data.get("type"),
                "host": data.get("host"),
                "matched_at": data.get("matched-at"),
                "severity": data.get("info", {}).get("severity", "info")
            })
        except json.JSONDecodeError:
            continue
            
    return {
        "findings": findings,
        "count": len(findings)
    }
