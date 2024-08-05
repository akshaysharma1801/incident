from django.db import models
import random
from django.utils import timezone
from apps.account.models import CustomUser

def generate_unique_incident_id():
    current_year = timezone.now().year
    while True:
        incident_id = f'RMG{random.randint(10000, 99999)}{current_year}'
        if not IncidentReport.objects.filter(incident_id=incident_id).exists():
            return incident_id
        
class IncidentReport(models.Model):
    ENTITY_CHOICES = [
        ('Enterprise', 'Enterprise'),
        ('Government', 'Government'),
    ]
    PRIORITY_CHOICES = [
        ('High', 'High'), 
        ('Medium', 'Medium'), 
        ('Low', 'Low')
    ]
    STATUS_CHOICES = [
        ('Open', 'Open'), 
        ('In progress', 'In progress'), 
        ('Closed', 'Closed')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='incidents')
    entity_type = models.CharField(max_length=10, choices=ENTITY_CHOICES)
    incident_details = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    incident_id = models.CharField(max_length=20, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.incident_id:
            self.incident_id = generate_unique_incident_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.incident_id