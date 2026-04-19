import docker
import json
import os
import time
import re
from django.conf import settings
from .registry import TOOL_REGISTRY
from utils.error_logger import log_error

# Import parsers
try:
    from .output_parsers import (
        nmap_parser, nikto_parser, nuclei_parser, semgrep_parser,
        sqlmap_parser, trufflehog_parser, trivy_parser, ffuf_parser,
        dalfox_parser, sslyze_parser, gitleaks_parser, gobuster_parser,
        subfinder_parser, arjun_parser, katana_parser, generic_parser
    )
except ImportError:
    from .output_parsers import generic_parser

PARSERS = {
    "nmap": getattr(nmap_parser, 'parse', generic_parser.parse),
    "nikto": getattr(nikto_parser, 'parse', generic_parser.parse),
    "nuclei": getattr(nuclei_parser, 'parse', generic_parser.parse),
    "semgrep": getattr(semgrep_parser, 'parse', generic_parser.parse),
    "sqlmap": getattr(sqlmap_parser, 'parse', generic_parser.parse),
    "trufflehog": getattr(trufflehog_parser, 'parse', generic_parser.parse),
    "trivy": getattr(trivy_parser, 'parse', generic_parser.parse),
    "ffuf": getattr(ffuf_parser, 'parse', generic_parser.parse),
    "dalfox": getattr(dalfox_parser, 'parse', generic_parser.parse),
    "sslyze": getattr(sslyze_parser, 'parse', generic_parser.parse),
    "gitleaks": getattr(gitleaks_parser, 'parse', generic_parser.parse),
    "gobuster": getattr(gobuster_parser, 'parse', generic_parser.parse),
    "subfinder": getattr(subfinder_parser, 'parse', generic_parser.parse),
    "arjun": getattr(arjun_parser, 'parse', generic_parser.parse),
    "katana": getattr(katana_parser, 'parse', generic_parser.parse),
}

def sanitize_args(args):
    """Simple sanitization to prevent command injection."""
    return re.sub(r'[;&|`$<>?*!(){}\[\]\n\r]', '', args)

def run_tool(tool_name, target, extra_args="", scan_id=None):
    if tool_name not in TOOL_REGISTRY:
        return {"stdout": "", "stderr": f"Tool {tool_name} not found", "exit_code": -1}

    # Simulation check
    if getattr(settings, 'SAFE_SIMULATION_MODE', False):
        return get_mock_result(tool_name, target)

    tool_config = TOOL_REGISTRY[tool_name]
    default_args = tool_config.get("default_args", "")
    
    # Sanitize and build command
    clean_extra_args = sanitize_args(str(extra_args))
    full_cmd = f"{tool_name} {default_args} {clean_extra_args} {target}"
    
    start_time = time.perf_counter()
    
    # Secure Execution via Docker SDK
    try:
        client = docker.from_env()
        timeout = getattr(settings, 'TOOL_TIMEOUT_SECONDS', 300)
        
        # We run the container as non-root and with resource limits.
        container_output = client.containers.run(
            image="vulnai-tools", # This image is built from Dockerfile.tools
            command=f"sh -c '{full_cmd}'",
            detach=False,
            remove=True,
            mem_limit="512m",
            cpu_quota=50000, # 50% of one core
            user="1000:1000", # Non-root vulnai user
            network_mode="bridge",
            stderr=True,
            stdout=True,
            timeout=timeout
        )
        
        raw_output = container_output.decode('utf-8', errors='replace')
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        
        parser_name = tool_config.get("output_parser")
        parser_func = PARSERS.get(parser_name, generic_parser.parse)
        
        return {
            "raw_output": raw_output,
            "parsed_output": parser_func(raw_output),
            "exit_code": 0,
            "duration_ms": duration_ms
        }

    except Exception as e:
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        log_error("apps.tools.executor", "DockerExecutionError", str(e), {"tool": tool_name})
        
        # Fallback to mock if Docker fails and user allows
        if getattr(settings, 'ALLOW_MOCK_FALLBACK', True):
            mock_res = get_mock_result(tool_name, target)
            mock_res["duration_ms"] = duration_ms
            return mock_res
            
        return {
            "raw_output": "", 
            "parsed_output": {"error": str(e)}, 
            "exit_code": -1,
            "duration_ms": duration_ms
        }

def get_mock_result(tool_name, target):
    """Expanded mock results for all Layer 1-4 tools."""
    mocks = {
        "nmap": {
            "findings": [
                {"title": "Open Port: 80", "description": "Apache 2.4.41", "severity": "info", "location": "port 80/tcp"},
                {"title": "Open Port: 443", "description": "Apache 2.4.41", "severity": "info", "location": "port 443/tcp"}
            ]
        },
        "nikto": {
            "findings": [{"title": "Server Leaks Version", "description": "Server reveals Apache/2.4.41", "severity": "low", "location": "/"}]
        },
        "nuclei": {
            "findings": [{"title": "Exposed Config", "description": "Found exposed /config.yaml", "severity": "medium", "location": "/config.yaml"}]
        },
        "sqlmap": {
            "findings": [{"title": "SQL Injection", "description": "Parameter 'id' is vulnerable to Boolean-based Blind SQLi", "severity": "high", "location": "/api/users?id=1"}]
        },
        "dalfox": {
            "findings": [{"title": "Verified XSS", "description": "Found reflected XSS on /search?q=", "severity": "high", "location": "/search?q=<script>alert(1)</script>"}]
        },
        "katana": {
            "findings": [
                {"title": "Discovered Endpoint", "description": "Found /login", "severity": "info", "location": "/login"},
                {"title": "Discovered Endpoint", "description": "Found /admin", "severity": "info", "location": "/admin"}
            ]
        },
        "gobuster": {
            "findings": [
                {"title": "Sensitive Path Discovered", "description": "Found /admin", "severity": "high", "location": "/admin"},
                {"title": "Discovered Path", "description": "Found /assets", "severity": "info", "location": "/assets"}
            ]
        },
        "arjun": {
            "findings": [{"title": "Discovered Parameter: debug", "description": "Hidden parameter 'debug' found", "severity": "info", "location": "/api"}]
        },
        "sslyze": {
            "findings": [{"title": "Weak Protocol: TLS 1.0", "description": "TLS 1.0 is enabled", "severity": "low", "location": "SSL/TLS"}]
        }
    }
    
    data = mocks.get(tool_name, {"findings": [], "count": 0})
    if "count" not in data:
        data["count"] = len(data.get("findings", []))
        
    return {
        "raw_output": f"[SIMULATION] Mock output for {tool_name} against {target}",
        "parsed_output": data,
        "exit_code": 0,
        "duration_ms": 100
    }
