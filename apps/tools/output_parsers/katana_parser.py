import re

def parse(raw_output: str) -> dict:
    """
    Parses Katana (crawler) output.
    Katana typically outputs found URLs one per line.
    """
    findings = []
    # Identify lines that look like URLs
    url_pattern = re.compile(r'https?://[^\s<>"]+')
    
    seen_urls = set()
    for line in raw_output.splitlines():
        match = url_pattern.search(line)
        if match:
            url = match.group(0)
            if url not in seen_urls:
                findings.append({
                    "title": "Discovered Endpoint",
                    "description": f"Crawled unique endpoint: {url}",
                    "severity": "info",
                    "location": url,
                    "evidence": line
                })
                seen_urls.add(url)
            
    return {
        "status": "success",
        "findings": findings,
        "count": len(findings),
        "summary": f"Crawled {len(findings)} unique endpoints"
    }
