def parse(raw_output: str) -> dict:
    # Minimal parsers for now to keep things moving
    return {"raw": raw_output[:1000], "count": 1}
