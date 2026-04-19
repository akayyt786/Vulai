#!/bin/bash
set -e

echo "-----------------------------------"
echo "VulnAI Phase 8 — Tool Bootstrap"
echo "-----------------------------------"

# 1. Database Migrations (Skip if SKIP_MIGRATIONS is set, e.g. during Docker build)
if [ "$SKIP_MIGRATIONS" != "1" ]; then
    echo "Running database migrations..."
    python3 manage.py migrate || echo "Migration failed (DB might be offline during build), skipping..."
fi

# 2. Update Nuclei Templates
if command -v nuclei &> /dev/null; then
    echo "Updating Nuclei templates..."
    nuclei -update-templates
fi

# 3. Check and verify major tools
TOOLS=("nmap" "nikto" "whatweb" "ffuf" "sqlmap" "nuclei" "subfinder" "katana" "dalfox" "trivy")
MISSING=0

for tool in "${TOOLS[@]}"; do
    if command -v $tool &> /dev/null; then
        echo "[OK] $tool is installed."
    else
        echo "[WARNING] $tool is NOT installed. Some scan layers may fail."
        MISSING=$((MISSING+1))
    fi
done

echo "-----------------------------------"
if [ $MISSING -eq 0 ]; then
    echo "Bootstrap complete. Environment is HEALTHY."
else
    echo "Bootstrap complete with $MISSING warnings. Please install missing tools for full coverage."
fi
echo "-----------------------------------"
