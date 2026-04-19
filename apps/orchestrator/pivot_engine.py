# Pivot types and logic for zero-findings scenarios

ATTACK_SURFACE_MATRIX = {
    "url": [
        "dns", "ports", "web_tech", "ssl", "directories", "parameters", 
        "vuln_scan", "sqli", "xss", "cors", "rce", "auth", "infrastructure"
    ],
    "repo": [
        "secrets", "dependencies", "static_analysis", "iac", "architecture", "logic"
    ]
}

def determine_pivot(context, last_result):
    """
    Suggests the next surface or layer when a tool returns no findings.
    context: current scan context
    last_result: output of the tool that just finished
    """
    input_type = context.get("input_type", "url")
    matrix = ATTACK_SURFACE_MATRIX.get(input_type, [])
    covered = context.get("surfaces_covered", [])
    
    # Simple logic: find the first surface in the matrix not yet covered
    for surface in matrix:
        if surface not in covered:
            return {
                "next_surface": surface,
                "strategy": "move_to_next_surface",
                "reasoning": f"Surface {surface} not yet tested."
            }
            
    # If all covered, suggest going deeper (e.g., Layer 6 chains)
    return {
        "strategy": "done",
        "reasoning": "All planned surfaces in the matrix have been covered."
    }
