FROM python:3.11-slim

# Install system dependencies and security tools
RUN apt-get update && apt-get install -y \
    nmap \
    whatweb \
    git \
    curl \
    wget \
    gnupg \
    sudo \
    golang \
    hydra \
    wafw00f \
    dnsrecon \
    && rm -rf /var/lib/apt/lists/*

# Install Nikto (source)
RUN git clone https://github.com/sullo/nikto.git /opt/nikto \
    && ln -s /opt/nikto/program/nikto.pl /usr/local/bin/nikto

# Set Go environment and install Go-based tools
ENV GOPATH=/root/go
ENV PATH=$PATH:/usr/local/go/bin:$GOPATH/bin

RUN go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install github.com/ffuf/ffuf@latest && \
    go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest && \
    go install github.com/haithamaouati/dalfox@latest && \
    go install github.com/projectdiscovery/katana/cmd/katana@latest && \
    go install github.com/zricethezav/gitleaks/v8@latest && \
    go install github.com/s0md3v/Arjun@latest && \
    go install github.com/OJ/gobuster/v3@latest && \
    go install github.com/epi052/feroxbuster/v2/cmd/feroxbuster@latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run bootstrap script if it exists
RUN if [ -f scripts/bootstrap.sh ]; then chmod +x scripts/bootstrap.sh && ./scripts/bootstrap.sh; fi

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
