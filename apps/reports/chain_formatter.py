from apps.scans.models import Finding

def format_chain_description(chain_finding):
    """
    Formats a human-readable description for an attack chain.
    """
    findings_ids = chain_finding.chained_from
    if not findings_ids:
        return f"Chain narrative: {chain_finding.description}"
        
    # Fetch titles and severities of the source findings
    source_findings = Finding.objects.filter(id__in=findings_ids)
    context_str = "\n".join([f"- [{f.severity.upper()}] {f.title}" for f in source_findings])
    
    return f"Attack Chain: {chain_finding.description}\n\nLinked Findings:\n{context_str}"
