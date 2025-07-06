from django.db import models
import uuid
import datetime
from apps.user.models import Apprentice


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Rotation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    duration = models.IntegerField()
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="rotations"
    )
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " " + self.department.name + " " + str(self.id)


class ApprenticeRotation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rotation = models.ForeignKey(
        Rotation, on_delete=models.CASCADE, related_name="apprentice_rotations"
    )
    apprentice = models.ForeignKey(
        Apprentice, on_delete=models.CASCADE, related_name="rotation_assignments"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("at_halt", "At Halt"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
        ],
        default="at_halt",
    )

    def __str__(self):
        return (
            self.rotation.name
            + " "
            + self.apprentice.user.first_name
            + " "
            + self.apprentice.user.last_name
        )
