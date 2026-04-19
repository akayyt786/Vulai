import re
import json

def parse(raw_output: str) -> dict:
    """
    Parses Arjun (parameter discovery) output.
    Attempts to parse JSON directly if -oJ was used, else uses regex.
    """
    findings = []
    params = []
    
    # Try parsing as JSON first
    try:
        # Search for JSON block in output
        json_match = re.search(r"(\{.*\})", raw_output, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(1))
            # Arjun JSON is usually { "url": { "params": { "get": [...], "post": [...] } } }
            for url, content in data.items():
                batch_params = []
                batch_params.extend(content.get("params", {}).get("get", []))
                batch_params.extend(content.get("params", {}).get("post", []))
                
                for p in list(set(batch_params)):
                    findings.append({
                        "title": f"Discovered Parameter: {p}",
                        "description": f"Hidden parameter '{p}' discovered on {url}",
                        "severity": "info",
                        "location": url,
                        "evidence": f"Found via JSON: {p}"
                    })
            return {"status": "success", "findings": findings, "count": len(findings)}
    except (json.JSONDecodeError, AttributeError):
        pass

    # Fallback to regex for stdout format: "Heuristic scan found 2 parameters: id, name"
    pattern = re.compile(r"parameters:\s*([\w, \s]+)")
    match = pattern.search(raw_output)
    if match:
        params = [p.strip() for p in match.group(1).split(',')]
        for p in params:
            findings.append({
                "title": f"Discovered Parameter: {p}",
                "description": f"Hidden parameter '{p}' discovered via heuristic scan.",
                "severity": "info",
                "location": "N/A",
                "evidence": f"Found via regex: {p}"
            })
            
    return {
        "status": "success",
        "findings": findings,
        "count": len(findings),
        "summary": f"Discovered {len(findings)} hidden parameters"
    }
