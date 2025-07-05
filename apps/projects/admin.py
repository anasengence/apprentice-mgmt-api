from django.contrib import admin
from .models import Project, MentorProject, ApprenticeProject

# Register your models here.
admin.site.register(Project)
admin.site.register(MentorProject)
admin.site.register(ApprenticeProject)
