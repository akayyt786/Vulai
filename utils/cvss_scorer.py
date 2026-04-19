def calculate_risk_score(findings):
    """
    Calculates a weighted CVSS-like risk score across all findings.
    findings: List of Finding model instances or dicts.
    """
    if not findings:
        return 0.0
    
    # Weighting factors for different severities
    weights = {
        'critical': 10.0,
        'high': 8.0,
        'medium': 5.0,
        'low': 2.0,
        'info': 0.0
    }
    
    total_score = 0.0
    count = 0
    
    for finding in findings:
        if isinstance(finding, dict):
            severity = finding.get('severity', 'info').lower()
            cvss_score = finding.get('cvss_score')
        else:
            severity = getattr(finding, 'severity', 'info').lower()
            cvss_score = getattr(finding, 'cvss_score', None)
            
        score = weights.get(severity, 0.0)
        if cvss_score is not None:
            score = float(cvss_score)
            
        total_score += score
        count += 1
        
    if count == 0:
        return 0.0
        
    # Final score is a weighted average or Cap at 10.0
    # For now, we take the highest score as the baseline and add small increments for others
    # to represent the total risk surface.
    findings_list = []
    for f in findings:
        if isinstance(f, dict):
            s = f.get('severity', 'info').lower()
            v = f.get('cvss_score')
        else:
            s = getattr(f, 'severity', 'info').lower()
            v = getattr(f, 'cvss_score', None)
        findings_list.append(v if v is not None else weights.get(s, 0.0))
        
    findings_list.sort(reverse=True)
    
    # Formula: Risk = Max(findings) + Sum(others) * 0.1, capped at 10.0
    base_score = findings_list[0]
    additional_risk = sum(findings_list[1:]) * 0.1
    
    final_score = min(10.0, base_score + additional_risk)
    
    return round(final_score, 1)

def severity_to_cvss_range(severity):
    """
    Returns a typical CVSS range for a given severity string.
    """
    severity = severity.lower()
    if severity == 'critical':
        return (9.0, 10.0)
    elif severity == 'high':
        return (7.0, 8.9)
    elif severity == 'medium':
        return (4.0, 6.9)
    elif severity == 'low':
        return (0.1, 3.9)
    else:
        return (0.0, 0.0)
