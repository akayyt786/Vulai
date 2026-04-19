import subprocess
from .registry import TOOL_REGISTRY
from utils.error_logger import log_error

def install_tool(tool_name):
    """
    Installs a security tool if not already present.
    Only allows installation of tools in TOOL_REGISTRY for security.
    """
    if tool_name not in TOOL_REGISTRY:
        log_error(
            "apps.tools.installer", "SecurityViolation",
            f"AI tried to install unlisted tool: {tool_name}"
        )
        return False

    tool_config = TOOL_REGISTRY[tool_name]
    
    # Check if already installed
    check_cmd = tool_config.get("check_command")
    if check_cmd:
        try:
            res = subprocess.run(check_cmd, shell=True, capture_output=True)
            if res.returncode == 0:
                return True # Already installed
        except Exception:
            pass
            
    # Install
    install_cmd = tool_config.get("install_command")
    if not install_cmd:
        return False
        
    try:
        process = subprocess.run(install_cmd, shell=True, capture_output=True, text=True)
        if process.returncode == 0:
            return True
        else:
            log_error(
                "apps.tools.installer", "ToolInstallError",
                f"Failed to install {tool_name}. Exit code: {process.returncode}",
                {"stdout": process.stdout, "stderr": process.stderr}
            )
            return False
    except Exception as e:
        log_error(
            "apps.tools.installer", "ToolInstallError",
            f"Exception during {tool_name} install: {str(e)}",
            exc=e
        )
        return False
