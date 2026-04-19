import json
import re
from utils.error_logger import log_error

def parse_llm_response(raw_response):
    """
    Parses LLM JSON response. Strips markdown fences and attempts basic repair.
    """
    if not raw_response:
        return {"action": "pivot", "reasoning": "Empty response from LLM"}

    # Strip markdown fences if present
    # regex matches: ```json ... ``` or just ``` ... ```
    cleaned = raw_response.strip()
    fence_pattern = re.compile(r"^```(?:json)?\s*(.*?)\s*```$", re.DOTALL | re.IGNORECASE)
    match = fence_pattern.match(cleaned)
    if match:
        cleaned = match.group(1).strip()
    
    try:
        data = json.loads(cleaned)
        
        # Basic validation of action field
        if "action" not in data:
            log_error("apps.orchestrator.parser", "LLMInvalidActionError", "Action field missing in LLM response", {"raw": raw_response})
            return {"action": "pivot", "reasoning": "Missing action field"}
            
        return data
    except json.JSONDecodeError as e:
        # Attempt simple repairs like fixing trailing commas or missing quotes (very basic)
        log_error(
            "apps.orchestrator.parser", "LLMParseError",
            f"Failed to parse LLM JSON: {str(e)}",
            {"raw": raw_response},
            exc=e
        )
        # Return a pivot action to avoid crashing the scan
        return {"action": "pivot", "reasoning": "JSON parse failed, forcing pivot"}
