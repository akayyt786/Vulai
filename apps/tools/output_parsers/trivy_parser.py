import json
def parse(raw_output: str) -> dict:
    try:
        data = json.loads(raw_output)
        return {"findings": data, "count": len(data)}
    except:
        return {"count": 1, "raw": raw_output[:500]}
