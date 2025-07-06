from django.db import models
import uuid
from apps.user.models import Apprentice, Mentor, User
from apps.projects.models import Project
from apps.rotation.models import Department

class BaseRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField()
    admin_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='%(class)s_reviewed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProjectJoinRequest(BaseRequest):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    apprentice = models.ForeignKey(Apprentice, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['apprentice', 'project', 'status']


class ProjectLeaveRequest(BaseRequest):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    apprentice = models.ForeignKey(Apprentice, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class RotationChangeRequest(BaseRequest):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    apprentice = models.ForeignKey(Apprentice, on_delete=models.CASCADE)
    current_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='rotation_change_from')
    requested_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='rotation_change_to')


class MentorLeaveRequest(BaseRequest):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class ApprenticeRemovalRequest(BaseRequest):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    apprentice = models.ForeignKey(Apprentice, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)