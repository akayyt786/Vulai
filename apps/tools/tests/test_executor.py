from django.test import TestCase
from unittest.mock import patch
from apps.tools.executor import run_tool

class ExecutorTest(TestCase):
    @patch('subprocess.run')
    def test_run_tool_success(self, mock_run):
        mock_run.return_value.stdout = "80/tcp open http"
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        
        result = run_tool("nmap", "http://example.com")
        self.assertEqual(result["exit_code"], 0)
        self.assertIn("findings", result["parsed_output"])
