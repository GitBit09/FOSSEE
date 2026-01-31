from django.db import models
from django.contrib.auth.models import User
import json


class Dataset(models.Model):
    """Store uploaded datasets with metadata"""
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    total_rows = models.IntegerField()
    summary_data = models.TextField()  # JSON string of summary statistics
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def set_summary(self, summary_dict):
        """Store summary as JSON"""
        self.summary_data = json.dumps(summary_dict)
    
    def get_summary(self):
        """Retrieve summary as dict"""
        return json.loads(self.summary_data) if self.summary_data else {}
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class Equipment(models.Model):
    """Store individual equipment records"""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment')
    equipment_name = models.CharField(max_length=200)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"
    
    class Meta:
        verbose_name_plural = "Equipment"
