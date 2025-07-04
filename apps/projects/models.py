import uuid
import datetime
from django.db import models

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(null=True, blank=True)
    trainer = models.ForeignKey("user.Trainer", on_delete=models.CASCADE, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_external = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name + " " + str(self.id)
