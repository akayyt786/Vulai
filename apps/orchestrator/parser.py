import json
import re
from utils.error_logger import log_error

def parse_llm_response(raw_response):
    """
    Parses LLM JSON response. Extracts the first JSON object found.
    """
    if not raw_response:
        return {"action": "pivot", "reasoning": "Empty response from LLM"}

    # Use regex to find the first '{' and the last '}'
    # This effectively strips <think> blocks or conversational filler
    try:
        match = re.search(r"(\{.*\})", raw_response, re.DOTALL)
        if not match:
            log_error("apps.orchestrator.parser", "LLMNoJsonError", "No JSON object found in response", {"raw": raw_response})
            return {"action": "pivot", "reasoning": "No valid JSON found"}
            
        cleaned = match.group(1).strip()
        data = json.loads(cleaned)
        
        # Basic validation of action field
        if "action" not in data:
            log_error("apps.orchestrator.parser", "LLMInvalidActionError", "Action field missing in LLM response", {"raw": raw_response})
            return {"action": "pivot", "reasoning": "Missing action field"}
            
        return data
    except (json.JSONDecodeError, AttributeError) as e:
        log_error(
            "apps.orchestrator.parser", "LLMParseError",
            f"Failed to parse LLM JSON: {str(e)}",
            {"raw": raw_response},
            exc=e
        )
        return {"action": "pivot", "reasoning": "JSON parse failed, forcing pivot"}
