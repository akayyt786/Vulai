#!/bin/bash
set -e

echo "Starting VulnAI Tool Bootstrap..."

# 1. Update Nuclei Templates
if command -v nuclei &> /dev/null; then
    echo "Updating Nuclei templates..."
    nuclei -update-templates
fi

# 2. Check major tools
TOOLS=("nmap" "nikto" "whatweb" "ffuf" "sqlmap" "nuclei" "subfinder")
for tool in "${TOOLS[@]}"; do
    if command -v $tool &> /dev/null; then
        echo "[OK] $tool is installed."
    else
        echo "[WARNING] $tool is NOT installed."
    fi
done

echo "Bootstrap complete."
