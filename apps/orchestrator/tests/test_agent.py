from django.test import TestCase
from unittest.mock import patch, MagicMock
from apps.scans.models import Scan, ScanStep
from apps.orchestrator.agent import OrchestratorAgent

class TestOrchestratorAgent(TestCase):
    def setUp(self):
        self.scan = Scan.objects.create(
            input_type="url",
            input_value="http://example.com",
            status="pending"
        )
        self.agent = OrchestratorAgent(self.scan.id)
        # Mock broadcast methods to avoid Redis dependency in tests
        self.agent._broadcast_status = MagicMock()
        self.agent._broadcast_step = MagicMock()
        self.agent._broadcast_completion = MagicMock()

    @patch('apps.orchestrator.agent.run_tool')
    @patch('apps.orchestrator.agent.LLMClient.call_llm')
    def test_run_scan_single_step(self, mock_llm, mock_run_tool):
        # 1. Mock LLM to run one tool then finish
        mock_llm.side_effect = [
            '{"action": "run_tool", "tool": "nmap", "surface": "ports", "layer": 1, "reasoning": "recon"}',
            '{"action": "done", "reasoning": "all finished"}'
        ]
        
        # 2. Mock tool result
        mock_run_tool.return_value = {
            "raw_output": "80/tcp open http",
            "parsed_output": {"findings": [{"title": "Port 80", "severity": "info"}]},
            "duration_ms": 100
        }
        
        # 3. Use determine_pivot mock to allow 'done'
        with patch('apps.orchestrator.pivot_engine.determine_pivot') as mock_pivot:
            mock_pivot.return_value = {"strategy": "done"}
            self.agent.run_scan()
        
        self.scan.refresh_from_db()
        self.assertEqual(self.scan.status, 'done')
        self.assertIn("ports", self.scan.surfaces_covered)
        self.assertEqual(ScanStep.objects.filter(scan=self.scan).count(), 1)

    @patch('apps.orchestrator.agent.LLMClient.call_llm')
    def test_process_findings_integration(self, mock_llm):
        # Mocking finding discovery
        step = ScanStep.objects.create(
            scan=self.scan,
            step_number=1,
            tool_name="nmap",
            layer=1,
            surface="ports"
        )
        
        parsed_data = {
            "findings": [
                {"title": "Found Port 80", "severity": "info", "location": "80/tcp"},
                {"title": "Found Port 443", "severity": "info", "location": "443/tcp"}
            ]
        }
        
        self.agent._process_findings(step, parsed_data)
        
        self.assertEqual(step.findings_count, 2)
        from apps.scans.models import Finding
        self.assertEqual(Finding.objects.filter(scan=self.scan).count(), 2)
