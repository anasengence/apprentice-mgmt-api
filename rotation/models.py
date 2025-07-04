from django.db import models
import uuid

class Rotation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    duration = models.IntegerField()
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    