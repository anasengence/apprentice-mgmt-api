from apps.projects.models import Project
from apps.user.models import Mentor, Apprentice
from django.db import models
import uuid

class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name="feedback")
    apprentice = models.ForeignKey(Apprentice, on_delete=models.CASCADE, related_name="feedback")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="feedback")
    satisfied = models.BooleanField(default=True)

    def __str__(self):
        return f"Feedback {self.id}" + " - " + self.apprentice.user.first_name + " " + self.mentor.user.first_name
    
    class Meta:
        ordering = ["-created_at"]
