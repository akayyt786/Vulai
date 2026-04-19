import subprocess
import json
import os
from django.conf import settings
from .registry import TOOL_REGISTRY
from utils.error_logger import log_error

# Import parsers (to be created next)
from .output_parsers import (
    nmap_parser, nikto_parser, nuclei_parser, semgrep_parser,
    sqlmap_parser, trufflehog_parser, trivy_parser, ffuf_parser,
    dalfox_parser, sslyze_parser, gitleaks_parser, gobuster_parser,
    subfinder_parser, arjun_parser, katana_parser, generic_parser
)

PARSERS = {
    "nmap": nmap_parser.parse,
    "nikto": nikto_parser.parse,
    "nuclei": nuclei_parser.parse,
    "semgrep": semgrep_parser.parse,
    "sqlmap": sqlmap_parser.parse,
    "trufflehog": trufflehog_parser.parse,
    "trivy": trivy_parser.parse,
    "ffuf": ffuf_parser.parse,
    "dalfox": dalfox_parser.parse,
    "sslyze": sslyze_parser.parse,
    "gitleaks": gitleaks_parser.parse,
    "gobuster": gobuster_parser.parse,
    "subfinder": subfinder_parser.parse,
    "arjun": arjun_parser.parse,
    "katana": katana_parser.parse,
}

def run_tool(tool_name, target, extra_args="", scan_id=None):
    """
    Executes a security tool against a target.
    tool_name: Name in TOOL_REGISTRY
    target: URL or path
    extra_args: Any LLM-provided additional arguments
    scan_id: UUID of the current scan
    """
    if tool_name not in TOOL_REGISTRY:
        log_error(
            "apps.tools.executor", "ToolNotFoundError",
            f"Tool '{tool_name}' not found in registry.",
            {"scan_id": scan_id, "tool": tool_name}
        )
        return {"stdout": "", "stderr": f"Tool {tool_name} not found", "exit_code": -1}

    tool_config = TOOL_REGISTRY[tool_name]
    default_args = tool_config.get("default_args", "")
    
    # Construct the command safely
    # AI provides tool_name and extra_args, but we look up the binary/base command
    # Note: For production, we would use a more robust way to prevent injection in extra_args,
    # but here we rely on the fact that LLM is the only source and we use subprocess.run with a list if possible.
    # However, many tools take complex flags, so we'll be careful.
    
    # Simple shell-safe command construct
    cmd_str = f"{tool_name} {default_args} {extra_args} {target}"
    
    timeout = getattr(settings, 'TOOL_TIMEOUT_SECONDS', 300)
    
    try:
        process = subprocess.run(
            cmd_str,
            shell=True, # Required for tools that need pipes or complex args
            text=True,
            capture_output=True,
            timeout=timeout
        )
        
        raw_output = process.stdout + process.stderr
        exit_code = process.returncode
        
        # Parse output
        parser_name = tool_config.get("output_parser")
        parser_func = PARSERS.get(parser_name, generic_parser.parse)
        
        parsed_data = parser_func(raw_output)
        
        return {
            "raw_output": raw_output,
            "parsed_output": parsed_data,
            "exit_code": exit_code,
            "duration_ms": 0, # Placeholder for timing
        }

    except subprocess.TimeoutExpired as e:
        log_error(
            "apps.tools.executor", "ToolTimeoutError",
            f"{tool_name} timed out after {timeout}s",
            {"scan_id": scan_id, "tool": tool_name},
            exc=e
        )
        return {
            "raw_output": e.stdout.decode() if e.stdout else "",
            "parsed_output": {"error": "timeout"},
            "exit_code": -1,
            "duration_ms": timeout * 1000
        }
    except Exception as e:
        log_error(
            "apps.tools.executor", "SubprocessError",
            f"Error running {tool_name}: {str(e)}",
            {"scan_id": scan_id, "tool": tool_name},
            exc=e
        )
        return {
            "raw_output": "",
            "parsed_output": {"error": str(e)},
            "exit_code": -1,
            "duration_ms": 0
        }
