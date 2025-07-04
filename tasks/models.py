from django.db import models
import uuid

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    mentor = models.ForeignKey("user.Mentor", on_delete=models.CASCADE, related_name="tasks")
    apprentice = models.ForeignKey("user.Apprentice", on_delete=models.CASCADE, related_name="tasks")
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
    
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"