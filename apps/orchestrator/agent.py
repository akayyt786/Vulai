from django.conf import settings
from apps.scans.models import Scan, ScanStep, Finding
from apps.tools.executor import run_tool
from apps.tools.installer import install_tool
from .llm_client import LLMClient
from .parser import parse_llm_response
from .context_manager import build_context
from .prompts import SYSTEM_PROMPT, build_user_prompt
from .chain_analyser import analyse_chains
from utils.error_logger import log_error

class OrchestratorAgent:
    def __init__(self, scan_id):
        self.scan_id = scan_id
        self.llm = LLMClient()
        self.max_steps = getattr(settings, 'MAX_SCAN_STEPS', 50)

    def run_scan(self):
        """
        Main loop for the autonomous scan.
        """
        scan = Scan.objects.get(id=self.scan_id)
        scan.status = 'running'
        scan.save()

        step_count = 0
        while step_count < self.max_steps:
            try:
                # 1. Build context
                context = build_context(self.scan_id)
                user_prompt = build_user_prompt(context)
                
                # 2. Call LLM
                raw_response = self.llm.call_llm(SYSTEM_PROMPT, user_prompt)
                action = parse_llm_response(raw_response)
                
                # 3. Handle Action
                if action["action"] == "run_tool":
                    tool = action.get("tool")
                    args = action.get("args")
                    surface = action.get("surface")
                    layer = action.get("layer")
                    
                    # Execute tool
                    result = run_tool(tool, scan.input_value, extra_args=args, scan_id=self.scan_id)
                    
                    # Create ScanStep
                    step = ScanStep.objects.create(
                        scan=scan,
                        step_number=step_count + 1,
                        layer=layer,
                        surface=surface,
                        tool_name=tool,
                        tool_args={"args": args},
                        raw_output=result.get("raw_output", ""),
                        parsed_output=result.get("parsed_output", {}),
                        findings_count=0, # Will be updated if findings discovered
                        ai_reasoning=action.get("reasoning", ""),
                        duration_ms=result.get("duration_ms", 0)
                    )
                    
                    # Process findings from result
                    self._process_findings(step, result.get("parsed_output", {}))
                    
                    # Update scan state
                    if surface not in scan.surfaces_covered:
                        scan.surfaces_covered.append(surface)
                        scan.save()
                    
                elif action["action"] == "install_tool":
                    tool = action.get("tool")
                    install_tool(tool)
                    # Don't increment step_count for installs? Or do? Let's say no.
                    continue

                elif action["action"] == "done":
                    break
                
                elif action["action"] == "pivot":
                    # Forcibly move to another surface if LLM is stuck/parsing failed
                    from .pivot_engine import determine_pivot
                    pivot = determine_pivot(context, {})
                    if pivot["strategy"] == "done":
                        break
                    # We continue the loop, the next iteration will have the pivot info in context?
                    # Actually, the pivot engine doesn't inject into LLM here, it just helps.
                    # We'll rely on the LLM to eventually say 'done'.
                    pass

                step_count += 1
                
                # Every 3 steps, run chain analysis
                if step_count % 3 == 0:
                    analyse_chains(self.scan_id)

            except Exception as e:
                log_error("apps.orchestrator.agent", "AgentError", str(e), {"scan_id": self.scan_id, "step": step_count}, exc=e)
                # Fail gracefully after 3 consecutive errors?
                break

        scan.status = 'done'
        scan.current_layer = context.get("current_layer", 1)
        scan.save()
        
        # Final chain analysis
        analyse_chains(self.scan_id)

    def _process_findings(self, step, parsed_data):
        """
        Extracts findings from tool output and saves them to DB.
        """
        # This logic varies by tool output structure.
        # Minimal implementation for now:
        findings_list = parsed_data.get("findings", [])
        for f_data in findings_list:
            Finding.objects.create(
                scan=step.scan,
                scan_step=step,
                title=f_data.get("title", f"Finding from {step.tool_name}"),
                description=f_data.get("description", ""),
                severity=f_data.get("severity", "info"),
                layer=step.layer,
                surface=step.surface,
                location=f_data.get("location", ""),
                evidence=f_data.get("evidence", "")
            )
        
        step.findings_count = len(findings_list)
        step.save()
