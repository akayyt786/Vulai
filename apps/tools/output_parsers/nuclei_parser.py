import json

def parse(raw_output: str) -> dict:
    findings = []
    for line in raw_output.splitlines():
        try:
            data = json.loads(line)
            info = data.get("info", {})
            findings.append({
                "title": info.get("name", data.get("template-id", "Nuclei Finding")),
                "description": info.get("description", "No description provided."),
                "severity": info.get("severity", "info"),
                "location": data.get("matched-at", data.get("host", ""))
            })
        except json.JSONDecodeError:
            continue
            
    return {"findings": findings, "count": len(findings)}
