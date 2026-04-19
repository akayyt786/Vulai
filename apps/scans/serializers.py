from rest_framework import serializers
from .models import Scan, ScanStep, Finding, Report

class FindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = '__all__'

class ScanStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanStep
        fields = ['step_number', 'layer', 'surface', 'tool_name', 'tool_args', 'findings_count', 'ai_reasoning', 'duration_ms', 'created_at']

class ScanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = ['input_type', 'input_value', 'consent_confirmed']
        
    def validate_consent_confirmed(self, value):
        if not value:
            raise serializers.ValidationError("Consent must be confirmed to proceed with the scan.")
        return value

class ScanStatusSerializer(serializers.ModelSerializer):
    steps = ScanStepSerializer(many=True, read_only=True)
    
    class Meta:
        model = Scan
        fields = ['id', 'status', 'current_layer', 'surfaces_covered', 'created_at', 'updated_at', 'steps']

class ScanDetailSerializer(serializers.ModelSerializer):
    findings = FindingSerializer(many=True, read_only=True)
    steps = ScanStepSerializer(many=True, read_only=True)
    
    class Meta:
        model = Scan
        fields = '__all__'
