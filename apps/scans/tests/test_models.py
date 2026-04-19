import uuid
from django.test import TestCase
from apps.scans.models import Scan, ScanStep, Finding

class ScanModelTest(TestCase):
    def test_scan_creation(self):
        scan = Scan.objects.create(
            input_type='url',
            input_value='http://example.com',
            consent_confirmed=True
        )
        self.assertEqual(scan.status, 'pending')
        self.assertIsInstance(scan.id, uuid.UUID)

    def test_scan_step_creation(self):
        scan = Scan.objects.create(input_type='url', input_value='http://example.com')
        step = ScanStep.objects.create(
            scan=scan,
            step_number=1,
            layer=1,
            surface='ports',
            tool_name='nmap'
        )
        self.assertEqual(step.tool_name, 'nmap')
