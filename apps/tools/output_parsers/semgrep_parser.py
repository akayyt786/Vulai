import json

def parse(raw_output: str) -> dict:
    """
    Parses semgrep JSON output.
    """
    try:
        data = json.loads(raw_output)
        results = data.get("results", [])
        findings = []
        for res in results:
            findings.append({
                "check_id": res.get("check_id"),
                "path": res.get("path"),
                "start": res.get("start", {}),
                "extra": {
                    "message": res.get("extra", {}).get("message"),
                    "severity": res.get("extra", {}).get("severity"),
                    "lines": res.get("extra", {}).get("lines")
                }
            })
        return {
            "findings": findings,
            "count": len(findings)
        }
    except json.JSONDecodeError:
        return {"error": "Failed to parse semgrep JSON output", "raw": raw_output[:1000]}
