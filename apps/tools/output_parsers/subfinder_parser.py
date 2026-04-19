def parse(raw_output: str) -> dict:
    return {"subdomains": raw_output.splitlines(), "count": len(raw_output.splitlines())}
