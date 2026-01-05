from django.contrib import admin
from .models import DiagnosticHistory

@admin.register(DiagnosticHistory)
class DiagnosticHistoryAdmin(admin.ModelAdmin):
    list_display = ['predicted_disease', 'confidence', 'symptoms', 'created_at']
    list_filter = ['predicted_disease', 'created_at']
    search_fields = ['symptoms', 'predicted_disease']
    readonly_fields = ['created_at']