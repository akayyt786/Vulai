FROM python:3.11-slim

# Install system dependencies and security tools (build-essential provides gcc for CGO)
RUN apt-get update && apt-get install -y \
    nmap \
    whatweb \
    git \
    curl \
    wget \
    gnupg \
    sudo \
    hydra \
    wafw00f \
    dnsrecon \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Go 1.22.2 (Debian slim ships old Go; projectdiscovery tools need 1.21+)
RUN wget -qO- https://go.dev/dl/go1.22.2.linux-amd64.tar.gz | tar -C /usr/local -xzf -

# Install Nikto from source (not available in slim repos)
RUN git clone https://github.com/sullo/nikto.git /opt/nikto \
    && ln -s /opt/nikto/program/nikto.pl /usr/local/bin/nikto

# Set Go environment
# CGO_ENABLED=1 is REQUIRED — trufflehog depends on go-tree-sitter which uses CGO
ENV GOPATH=/root/go
ENV PATH=$PATH:/usr/local/go/bin:$GOPATH/bin
ENV CGO_ENABLED=1

# Install Go-based security tools
# NOTE: feroxbuster is Rust (not Go) — excluded
# NOTE: Arjun is Python (not Go) — installed via pip in requirements.txt
RUN go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install github.com/ffuf/ffuf@latest && \
    go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest && \
    go install github.com/hahwul/dalfox/v2@latest && \
    go install github.com/projectdiscovery/katana/cmd/katana@latest && \
    go install github.com/zricethezav/gitleaks/v8@latest && \
    go install github.com/OJ/gobuster/v3@latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run bootstrap script if it exists (skip migrations during build)
RUN SKIP_MIGRATIONS=1; export SKIP_MIGRATIONS; \
    if [ -f scripts/bootstrap.sh ]; then chmod +x scripts/bootstrap.sh && ./scripts/bootstrap.sh; fi

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
