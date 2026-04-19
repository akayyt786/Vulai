import uuid
from django.db import models

class Scan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    input_type = models.CharField(max_length=10, choices=[('url', 'url'), ('repo', 'repo'), ('file', 'file')])
    input_value = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'pending'), ('running', 'running'), ('done', 'done'), ('failed', 'failed')],
        default='pending'
    )
    current_layer = models.IntegerField(default=1)
    surfaces_covered = models.JSONField(default=list)
    consent_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Scan {self.id} ({self.input_type})"

class ScanStep(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scan = models.ForeignKey('Scan', on_delete=models.CASCADE, related_name='steps')
    step_number = models.IntegerField()
    layer = models.IntegerField()
    surface = models.CharField(max_length=100)
    tool_name = models.CharField(max_length=100)
    tool_args = models.JSONField(default=dict)
    raw_output = models.TextField(blank=True)
    parsed_output = models.JSONField(default=dict)
    findings_count = models.IntegerField(default=0)
    ai_reasoning = models.TextField(blank=True)
    pivot_reason = models.TextField(blank=True)
    duration_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ScanStep {self.step_number} for {self.scan_id}"

class Finding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scan = models.ForeignKey('Scan', on_delete=models.CASCADE, related_name='findings')
    scan_step = models.ForeignKey('ScanStep', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(
        max_length=10,
        choices=[
            ('critical', 'critical'),
            ('high', 'high'),
            ('medium', 'medium'),
            ('low', 'low'),
            ('info', 'info')
        ]
    )
    cvss_score = models.FloatField(null=True, blank=True)
    cvss_vector = models.CharField(max_length=100, blank=True)
    cve_id = models.CharField(max_length=30, blank=True)
    cwe_id = models.CharField(max_length=20, blank=True)
    layer = models.IntegerField()
    surface = models.CharField(max_length=100)
    location = models.CharField(max_length=500, blank=True)
    evidence = models.TextField(blank=True)
    remediation = models.TextField(blank=True)
    is_chained = models.BooleanField(default=False)
    chained_from = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.severity.upper()} - {self.title}"

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scan = models.OneToOneField('Scan', on_delete=models.CASCADE)
    summary = models.TextField()
    attack_narrative = models.TextField()
    findings_count = models.JSONField(default=dict)
    surfaces_tested = models.JSONField(default=list)
    chains_found = models.JSONField(default=list)
    risk_score = models.FloatField(default=0.0)
    raw_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.scan_id}"
