TOOL_REGISTRY = {
    # --- Layer 1: Reconnaissance ---
    "nmap": {
        "description": "Port and service discovery",
        "install_method": "apt",
        "install_command": "apt-get install -y nmap",
        "check_command": "nmap --version",
        "applicable_to": ["url"],
        "layer": 1,
        "surface": "ports",
        "output_parser": "nmap",
        "default_args": "-sV -sC -T4"
    },
    "dnsrecon": {
        "description": "DNS record enumeration",
        "install_method": "pip",
        "install_command": "pip install dnsrecon",
        "check_command": "dnsrecon --version",
        "applicable_to": ["url"],
        "layer": 1,
        "surface": "dns",
        "output_parser": "dnsrecon",
        "default_args": "-d"
    },
    "subfinder": {
        "description": "Subdomain discovery",
        "install_method": "go",
        "install_command": "go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
        "check_command": "subfinder --version",
        "applicable_to": ["url"],
        "layer": 1,
        "surface": "dns",
        "output_parser": "subfinder",
        "default_args": "-silent -d"
    },
    "whatweb": {
        "description": "Web technology fingerprinting",
        "install_method": "apt",
        "install_command": "apt-get install -y whatweb",
        "check_command": "whatweb --version",
        "applicable_to": ["url"],
        "layer": 1,
        "surface": "web_tech",
        "output_parser": "whatweb",
        "default_args": "--color=never"
    },
    "wafw00f": {
        "description": "WAF detection",
        "install_method": "pip",
        "install_command": "pip install wafw00f",
        "check_command": "wafw00f --version",
        "applicable_to": ["url"],
        "layer": 1,
        "surface": "waf",
        "output_parser": "wafw00f",
        "default_args": ""
    },
    "sslyze": {
        "description": "SSL/TLS configuration analysis",
        "install_method": "pip",
        "install_command": "pip install sslyze",
        "check_command": "sslyze --version",
        "applicable_to": ["url"],
        "layer": 1,
        "surface": "ssl",
        "output_parser": "sslyze",
        "default_args": "--regular"
    },

    # --- Layer 2: Surface Mapping ---
    "ffuf": {
        "description": "Directory/file/parameter fuzzing",
        "install_method": "go",
        "install_command": "go install github.com/ffuf/ffuf@latest",
        "check_command": "ffuf -V",
        "applicable_to": ["url"],
        "layer": 2,
        "surface": "directories",
        "output_parser": "ffuf",
        "default_args": "-mc 200,301,302 -w /usr/share/wordlists/dirb/common.txt -u"
    },
    "gobuster": {
        "description": "Directory brute-force",
        "install_method": "go",
        "install_command": "go install github.com/OJ/gobuster/v3@latest",
        "check_command": "gobuster version",
        "applicable_to": ["url"],
        "layer": 2,
        "surface": "directories",
        "output_parser": "gobuster",
        "default_args": "dir -w /usr/share/wordlists/dirb/common.txt -u"
    },
    "arjun": {
        "description": "HTTP parameter discovery",
        "install_method": "pip",
        "install_command": "pip install arjun",
        "check_command": "arjun --version",
        "applicable_to": ["url"],
        "layer": 2,
        "surface": "parameters",
        "output_parser": "arjun",
        "default_args": "-u"
    },
    "katana": {
        "description": "Web crawler",
        "install_method": "go",
        "install_command": "go install github.com/projectdiscovery/katana/cmd/katana@latest",
        "check_command": "katana --version",
        "applicable_to": ["url"],
        "layer": 2,
        "surface": "crawl",
        "output_parser": "katana",
        "default_args": "-silent -u"
    },

    # --- Layer 3: Vulnerability Detection ---
    "nikto": {
        "description": "Web server vulnerability scan",
        "install_method": "apt",
        "install_command": "apt-get install -y nikto",
        "check_command": "nikto -Version",
        "applicable_to": ["url"],
        "layer": 3,
        "surface": "web_vuln",
        "output_parser": "nikto",
        "default_args": "-host"
    },
    "nuclei": {
        "description": "Template-based vulnerability scanner",
        "install_method": "go",
        "install_command": "go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
        "check_command": "nuclei --version",
        "applicable_to": ["url", "repo"],
        "layer": 3,
        "surface": "vuln_scan",
        "output_parser": "nuclei",
        "default_args": "-silent -u"
    },
    "sqlmap": {
        "description": "SQL injection detection",
        "install_method": "pip",
        "install_command": "pip install sqlmap",
        "check_command": "sqlmap --version",
        "applicable_to": ["url"],
        "layer": 3,
        "surface": "sqli",
        "output_parser": "sqlmap",
        "default_args": "--batch --risk=1 --level=3 --random-agent -u"
    },
    "dalfox": {
        "description": "XSS parameter analysis",
        "install_method": "go",
        "install_command": "go install github.com/haithamaouati/dalfox@latest",
        "check_command": "dalfox version",
        "applicable_to": ["url"],
        "layer": 3,
        "surface": "xss",
        "output_parser": "dalfox",
        "default_args": "url"
    },
    "commix": {
        "description": "Command injection testing",
        "install_method": "pip",
        "install_command": "pip install commix",
        "check_command": "commix --version",
        "applicable_to": ["url"],
        "layer": 3,
        "surface": "rce",
        "output_parser": "commix",
        "default_args": "--batch --user-agent=VulnAI -u"
    },
    "corsy": {
        "description": "CORS misconfiguration scanner",
        "install_method": "pip",
        "install_command": "pip install corsy",
        "check_command": "corsy --version",
        "applicable_to": ["url"],
        "layer": 3,
        "surface": "cors",
        "output_parser": "corsy",
        "default_args": "-u"
    },

    # --- Code Analysis & Secrets (Repo/File) ---
    "semgrep": {
        "description": "Multi-language static analysis",
        "install_method": "pip",
        "install_command": "pip install semgrep",
        "check_command": "semgrep --version",
        "applicable_to": ["repo", "file"],
        "layer": 3,
        "surface": "static_analysis",
        "output_parser": "semgrep",
        "default_args": "scan --json --config auto"
    },
    "bandit": {
        "description": "Python security linting",
        "install_method": "pip",
        "install_command": "pip install bandit",
        "check_command": "bandit --version",
        "applicable_to": ["repo", "file"],
        "layer": 3,
        "surface": "python_sec",
        "output_parser": "bandit",
        "default_args": "-r -f json"
    },
    "trufflehog": {
        "description": "Secret scanning",
        "install_method": "go",
        "install_command": "go install github.com/trufflesecurity/trufflehog/v3@latest",
        "check_command": "trufflehog version",
        "applicable_to": ["repo", "file"],
        "layer": 1,
        "surface": "secrets",
        "output_parser": "trufflehog",
        "default_args": "github --json --repo"
    },
    "gitleaks": {
        "description": "Secret detection in git repos",
        "install_method": "go",
        "install_command": "go install github.com/zricethezav/gitleaks/v8@latest",
        "check_command": "gitleaks version",
        "applicable_to": ["repo"],
        "layer": 1,
        "surface": "secrets",
        "output_parser": "gitleaks",
        "default_args": "detect --no-banner --report-format json --source"
    },
    "trivy": {
        "description": "CVE scan for packages and IaC",
        "install_method": "apt",
        "install_command": "apt-get install -y trivy",
        "check_command": "trivy --version",
        "applicable_to": ["repo", "file"],
        "layer": 2,
        "surface": "dependencies",
        "output_parser": "trivy",
        "default_args": "repo --format json"
    },
    "checkov": {
        "description": "IaC security analysis",
        "install_method": "pip",
        "install_command": "pip install checkov",
        "check_command": "checkov --version",
        "applicable_to": ["repo", "file"],
        "layer": 4,
        "surface": "iac",
        "output_parser": "checkov",
        "default_args": "-d"
    }
}
