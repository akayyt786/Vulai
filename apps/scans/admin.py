from django.contrib import admin
from .models import Scan, ScanStep, Finding, Report

@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ('id', 'input_type', 'status', 'current_layer', 'created_at')
    list_filter = ('input_type', 'status')
    search_fields = ('id', 'input_value')

@admin.register(ScanStep)
class ScanStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'scan', 'step_number', 'layer', 'surface', 'tool_name', 'findings_count')
    list_filter = ('layer', 'surface', 'tool_name')
    search_fields = ('scan__id', 'tool_name')

@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = ('id', 'scan', 'title', 'severity', 'layer', 'surface', 'is_chained')
    list_filter = ('severity', 'layer', 'surface', 'is_chained')
    search_fields = ('scan__id', 'title', 'description')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'scan', 'risk_score', 'created_at')
    search_fields = ('scan__id', 'summary')
