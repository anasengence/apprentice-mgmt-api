from django.contrib import admin
from .models import (
    ProjectJoinRequest,
    ProjectLeaveRequest,
    RotationChangeRequest,
    MentorLeaveRequest,
    ApprenticeRemovalRequest,
)

admin.site.register(ProjectJoinRequest)
admin.site.register(ProjectLeaveRequest)
admin.site.register(RotationChangeRequest)
admin.site.register(MentorLeaveRequest)
admin.site.register(ApprenticeRemovalRequest)
