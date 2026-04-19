# Pivot types and logic for zero-findings scenarios

ATTACK_SURFACE_MATRIX = {
    "url": {
        1: ["dns", "ports", "web_tech", "ssl", "headers", "certs"],
        2: ["directories", "api_endpoints", "subdomains", "parameters", "js_analysis", "robots", "crawl"],
        3: ["vuln_scan", "sqli", "xss", "ssti", "ssrf", "xxe", "open_redirect", "cors", "clickjacking", "csrf", "traversal", "file_inclusion", "cmd_injection"],
        4: ["brute_force", "default_creds", "jwt_analysis", "oauth", "pw_reset", "session_fixation", "cookie_flags"],
        5: ["waf", "cdn", "cloud_metadata", "admin_panel", "backup_exposure", "source_disclosure", "error_pages"],
        6: ["chain_analysis", "targeted_payloads"]
    },
    "repo": {
        1: ["git_history", "live_files", "api_keys", "private_keys", "env_files", "cloud_creds"],
        2: ["vuln_audit", "outdated_audit", "malicious_detection", "license_risk", "transitive_cves"],
        3: ["general_vulns", "python", "javascript", "java", "go", "php", "ruby", "cpp", "deserialization", "mass_assignment", "race_conditions", "crypto"],
        4: ["docker", "docker_compose", "kubernetes", "terraform", "github_actions", "cloudformation", "helm"],
        5: ["hardcoded_data", "debug_mode", "random_usage", "input_validation", "redos", "proto_pollution", "sql_construction", "cmd_construction", "path_construction", "permissions", "logging", "jwt_strength", "hashing", "cors_wildcard"],
        6: ["privilege_escalation", "idor", "rate_limiting", "mass_assignment_risk", "payment_logic", "isolation"]
    }
}

def determine_pivot(context, last_result):
    """
    Suggests the next surface or layer when a tool returns no findings.
    """
    input_type = context.get("input_type", "url")
    matrix = ATTACK_SURFACE_MATRIX.get(input_type, {})
    covered = context.get("surfaces_covered", [])
    current_layer = context.get("current_layer", 1)
    
    # Check current layer first
    for layer in range(current_layer, 7):
        surfaces = matrix.get(layer, [])
        for surface in surfaces:
            if surface not in covered:
                return {
                    "next_surface": surface,
                    "next_layer": layer,
                    "strategy": "move_to_next_surface",
                    "reasoning": f"Surface {surface} in Layer {layer} not yet tested."
                }
            
    return {
        "strategy": "done",
        "reasoning": "All planned surfaces in the matrix have been covered."
    }
