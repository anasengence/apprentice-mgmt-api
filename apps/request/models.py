from django.db import models
import uuid
from apps.user.models import Apprentice, Trainer
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    apprentice = models.ForeignKey(
        Apprentice, on_delete=models.CASCADE, related_name="requests"
    )
    processed_by = models.ForeignKey(
        Trainer, on_delete=models.CASCADE, related_name="processed_requests"
    )
    # Generic ForeignKey to either a Rotation or Project
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_object_id = models.UUIDField()
    target = GenericForeignKey("target_content_type", "target_object_id")
