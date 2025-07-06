import uuid
import datetime
from django.db import models


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(null=True, blank=True)
    trainer = models.ForeignKey(
        "user.Trainer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_external = models.BooleanField(default=False)
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
        return self.name + " " + str(self.id)

    class Meta:
        ordering = ["-created_at"]


class ApprenticeProject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="apprentices_projects"
    )
    apprentice = models.ForeignKey(
        "user.Apprentice", on_delete=models.CASCADE, related_name="projects_apprentices"
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    joined_at = models.DateField(default=datetime.date.today)
    left_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return (
            self.project.name
            + " "
            + self.apprentice.user.first_name
            + " "
            + self.apprentice.user.last_name
        )

    class Meta:
        ordering = ["-created_at"]


class MentorProject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="mentors_projects"
    )
    mentor = models.ForeignKey(
        "user.Mentor", on_delete=models.CASCADE, related_name="projects_mentors"
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    joined_at = models.DateField(default=datetime.date.today)
    left_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return (
            self.project.name
            + " "
            + self.mentor.user.first_name
            + " "
            + self.mentor.user.last_name
        )

    class Meta:
        ordering = ["-created_at"]
