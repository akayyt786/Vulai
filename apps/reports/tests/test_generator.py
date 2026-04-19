import unittest
from unittest.mock import MagicMock, patch
from apps.reports.generator import generate_report
from apps.scans.models import Scan, Finding, Report
from django.test import TestCase

class TestReportGenerator(TestCase):
    def setUp(self):
        self.scan = Scan.objects.create(
            input_type="url",
            input_value="http://example.com",
            status="done",
            surfaces_covered=["dns", "ports"]
        )
        Finding.objects.create(
            scan=self.scan,
            title="Open Port: 80",
            severity="info",
            location="Port 80",
            description="Web server detected",
            layer=1,
            surface="ports"
        )
        Finding.objects.create(
            scan=self.scan,
            title="SQL Injection",
            severity="critical",
            location="/api/login",
            description="Vulnerable to SQLi",
            layer=3,
            surface="sqli"
        )

    @patch('apps.orchestrator.llm_client.LLMClient.call_llm')
    def test_generate_report_success(self, mock_llm):
        mock_llm.return_value = '{"action": "report", "summary": "Test Summary", "narrative": "Test Narrative"}'
        
        report = generate_report(self.scan.id)
        
        self.assertIsNotNone(report)
        self.assertEqual(report.summary, "Test Summary")
        self.assertEqual(report.attack_narrative, "Test Narrative")
        self.assertEqual(report.findings_count["critical"], 1)
        self.assertEqual(report.findings_count["info"], 1)
        self.assertTrue(report.risk_score > 9.0) # Critical find should push it high

    def test_generate_report_no_scan(self):
        report = generate_report("non-existent-id")
        self.assertIsNone(report)
