def format_chain_description(chain_finding):
    """
    Formats a human-readable description for an attack chain.
    """
    findings_ids = chain_finding.chained_from
    description = chain_finding.description
    
    # This can be expanded to include more details from the source findings
    return f"Attack Chain: {description}\nChained from findings: {', '.join(findings_ids)}"
 Broadway
