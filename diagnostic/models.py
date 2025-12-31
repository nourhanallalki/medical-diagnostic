from django.db import models
from django.contrib.auth.models import User

class DiagnosticHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    symptoms = models.TextField()
    predicted_disease = models.CharField(max_length=200)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Historique de diagnostic'
        verbose_name_plural = 'Historiques de diagnostic'
    
    def __str__(self):
        return f"{self.predicted_disease} - {self.confidence}% ({self.created_at.strftime('%d/%m/%Y')})"