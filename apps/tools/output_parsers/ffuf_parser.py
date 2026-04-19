import json

def parse(raw_output: str) -> dict:
    """
    Parses ffuf JSON output.
    """
    try:
        data = json.loads(raw_output)
        results = data.get("results", [])
        found_paths = [{"url": r.get("url"), "status": r.get("status")} for r in results]
        return {
            "discovered_paths": found_paths,
            "count": len(found_paths)
        }
    except json.JSONDecodeError:
        # Fallback for non-JSON output
        lines = raw_output.splitlines()
        return {"count": len(lines), "raw": lines[:10]}
