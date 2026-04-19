from rest_framework import serializers
from .models import Scan, ScanStep, Finding, Report
from urllib.parse import urlparse

class FindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = [
            'id', 'title', 'description', 'severity', 'cvss_score', 
            'cve_id', 'cwe_id', 'layer', 'surface', 'location', 
            'evidence', 'remediation', 'is_chained', 'chained_from', 'created_at'
        ]

class ScanStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanStep
        fields = [
            'step_number', 'layer', 'surface', 'tool_name', 
            'findings_count', 'ai_reasoning', 'duration_ms', 'created_at'
        ]

class ScanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = ['input_type', 'input_value', 'consent_confirmed']
        
    def validate_consent_confirmed(self, value):
        from django.conf import settings
        if getattr(settings, 'REQUIRE_CONSENT', True) and not value:
            raise serializers.ValidationError("Consent must be confirmed to proceed with the scan.")
        return value

    def validate(self, data):
        input_type = data.get('input_type')
        input_value = data.get('input_value')

        if input_type == 'url':
            parsed = urlparse(input_value)
            if not all([parsed.scheme, parsed.netloc]):
                raise serializers.ValidationError({"input_value": "Provide a valid URL (e.g., https://target.com)"})
        elif input_type == 'repo':
            if not (input_value.startswith('http') and input_value.endswith('.git')):
                raise serializers.ValidationError({"input_value": "Provide a valid Git repository URL (e.g., https://github.com/user/repo.git)"})
        
        return data

class ScanStatusSerializer(serializers.ModelSerializer):
    scan_id = serializers.UUIDField(source='id', read_only=True)
    steps = ScanStepSerializer(many=True, read_only=True)
    
    class Meta:
        model = Scan
        fields = [
            'scan_id', 'status', 'input_type', 'input_value', 
            'current_layer', 'surfaces_covered', 'created_at', 'updated_at', 'steps'
        ]

class ScanDetailSerializer(serializers.ModelSerializer):
    scan_id = serializers.UUIDField(source='id', read_only=True)
    findings = FindingSerializer(many=True, read_only=True)
    steps = ScanStepSerializer(many=True, read_only=True)
    
    class Meta:
        model = Scan
        fields = [
            'scan_id', 'input_type', 'input_value', 'status', 
            'current_layer', 'surfaces_covered', 'created_at', 'updated_at', 'findings', 'steps'
        ]
