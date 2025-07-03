# users/admin.py
from django.contrib import admin
from .models import User, Apprentice, Mentor, Trainer

admin.site.register(User)
admin.site.register(Apprentice)
admin.site.register(Mentor)
admin.site.register(Trainer)