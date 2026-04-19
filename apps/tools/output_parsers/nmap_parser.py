import re

def parse(raw_output: str) -> dict:
    """
    Parses nmap output to find open ports and services.
    """
    found = []
    # Pattern for "80/tcp open  http"
    pattern = re.compile(r"(\d+)/(tcp|udp)\s+open\s+(\S+)\s*(.*)")
    
    for line in raw_output.splitlines():
        match = pattern.search(line)
        if match:
            found.append({
                "port": match.group(1),
                "protocol": match.group(2),
                "service": match.group(3),
                "version": match.group(4).strip()
            })
            
    return {
        "open_ports": found,
        "count": len(found)
    }
