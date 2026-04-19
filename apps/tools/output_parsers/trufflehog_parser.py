import json

def parse(raw_output: str) -> dict:
    """
    Parses trufflehog JSON output into standardized findings.
    """
    findings = []
    for line in raw_output.splitlines():
        if not line.strip(): continue
        try:
            data = json.loads(line)
            # Trufflehog V3 output
            detector = data.get("DetectorName", "Credential")
            source_metadata = data.get("SourceMetadata", {}).get("Data", {})
            file_path = source_metadata.get("Github", {}).get("file", source_metadata.get("Git", {}).get("file", "Unknown"))
            line_num = source_metadata.get("Github", {}).get("line", 0)

            findings.append({
                "title": f"Secret Exposed: {detector}",
                "description": f"Potential credentials or sensitive data leaked via {detector} detector.",
                "severity": "high", # Credential leaks are always high/critical
                "location": f"{file_path}:{line_num}",
                "evidence": f"Redacted Secret: {data.get('Raw', '')[:10]}..."
            })
        except json.JSONDecodeError:
            continue
            
    return {
        "findings": findings,
        "count": len(findings)
    }
