import json

def parse(raw_output: str) -> dict:
    """
    Parses trufflehog JSON output.
    """
    findings = []
    for line in raw_output.splitlines():
        try:
            data = json.loads(line)
            findings.append({
                "source_id": data.get("SourceID"),
                "detector_name": data.get("DetectorName"),
                "raw": data.get("Raw", "")[:50] + "...",
                "file": data.get("SourceMetadata", {}).get("Data", {}).get("Github", {}).get("file")
            })
        except json.JSONDecodeError:
            continue
            
    return {
        "findings": findings,
        "count": len(findings)
    }
