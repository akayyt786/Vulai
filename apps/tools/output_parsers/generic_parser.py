def parse(raw_output: str) -> dict:
    """
    Generic fallback parser.
    """
    lines = raw_output.splitlines()
    return {
        "count": len(lines),
        "raw_lines": lines[:100], # Cap for DB safety
        "total_chars": len(raw_output)
    }
