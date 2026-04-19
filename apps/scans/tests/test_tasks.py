from django.test import TestCase
from unittest.mock import patch, MagicMock
from apps.scans.models import Scan
from apps.scans.tasks import run_scan_task

class TestScanTasks(TestCase):
    def setUp(self):
        self.scan = Scan.objects.create(
            input_type="url",
            input_value="http://example.com",
            status="pending"
        )

    @patch('apps.scans.tasks.OrchestratorAgent.run_scan')
    @patch('apps.scans.tasks.generate_report')
    def test_run_scan_task_success(self, mock_report, mock_run):
        run_scan_task(self.scan.id)
        
        # Verify agent ran
        mock_run.assert_called_once()
        # Verify report generation was triggered
        mock_report.assert_called_once_with(self.scan.id)
        
    @patch('apps.scans.tasks.OrchestratorAgent.run_scan')
    def test_run_scan_task_failure(self, mock_run):
        mock_run.side_effect = Exception("Agent crashed")
        
        with self.assertRaises(Exception):
            run_scan_task(self.scan.id)
            
        self.scan.refresh_from_db()
        self.assertEqual(self.scan.status, 'failed')
