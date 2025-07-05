from django.contrib import admin
from .models import Department, Rotation, ApprenticeRotation

admin.site.register(Department)
admin.site.register(Rotation)
admin.site.register(ApprenticeRotation)
