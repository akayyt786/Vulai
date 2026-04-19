import traceback
from datetime import datetime, timezone
from pathlib import Path

# Updated path to match the project structure
ERRORS_PATH = Path(__file__).parent.parent / "docs" / "ERRORS.md"
MARKER = "<!-- RUNTIME LOG START -->"

def log_error(
    component: str,
    error_type: str,
    message: str,
    context: dict = None,
    exc: Exception = None
):
    """
    component:  dotted module path e.g. "apps.orchestrator.agent"
    error_type: class name e.g. "ToolTimeoutError"
    message:    what went wrong in plain English
    context:    dict with scan_id, tool, surface, step_number etc.
    exc:        the caught exception or None
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    tb = (
        "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        if exc else "No exception — manual log entry"
    )
    ctx = "\n".join(f"  {k}: {v}" for k, v in (context or {}).items())

    entry = (
        f"\n---\n\n"
        f"### [{timestamp}] {error_type} in {component}\n\n"
        f"**Message:** {message}\n\n"
        f"**Context:**\n{ctx or '  none'}\n\n"
        f"**Traceback:**\n```\n{tb}\n```\n\n"
        f"**Status:** open\n"
    )

    try:
        if not ERRORS_PATH.exists():
            ERRORS_PATH.parent.mkdir(parents=True, exist_ok=True)
            ERRORS_PATH.write_text(f"# ERRORS.md — VulnAI Runtime Error Log\n\n{MARKER}\n", encoding="utf-8")

        text = ERRORS_PATH.read_text(encoding="utf-8")
        if MARKER not in text:
            text += f"\n{MARKER}\n"
        ERRORS_PATH.write_text(text + entry, encoding="utf-8")
    except Exception as e:
        # Fallback to stderr if file write fails
        import sys
        print(f"CRITICAL: Failed to log error to {ERRORS_PATH}: {e}", file=sys.stderr)
        print(entry, file=sys.stderr)
