from rest_framework import serializers
from apps.scans.models import Report, Finding
from apps.scans.serializers import FindingSerializer

class ReportSerializer(serializers.ModelSerializer):
    scan_id = serializers.UUIDField(source='scan.id', read_only=True)
    chains = serializers.JSONField(source='chains_found', read_only=True)
    findings = serializers.SerializerMethodField()
    
    class Meta:
        model = Report
        fields = [
            'scan_id', 'summary', 'attack_narrative', 'risk_score', 
            'findings_count', 'surfaces_tested', 'chains', 
            'findings', 'raw_json', 'created_at'
        ]
        
    def get_findings(self, obj):
        findings = Finding.objects.filter(scan=obj.scan).order_by('-severity', 'title')
        return FindingSerializer(findings, many=True).data
