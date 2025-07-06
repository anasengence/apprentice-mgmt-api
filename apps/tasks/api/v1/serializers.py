from rest_framework import serializers
from apps.tasks.models import Task
import datetime

class TaskReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "assigned_by",
            "assigned_to",
            "project",
            "assigned_at",
            "due_date",
            "completed_at",
            "created_at",
            "updated_at",
        ]


class TaskWriteSerializer(TaskReadSerializer):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "assigned_to",
            "project",
            "due_date",
            "completed_at",
        ]
    
    def create(self, validated_data):
        validated_data["assigned_by"] = self.context["request"].user
        validated_data["created_at"] = datetime.date.today()
        validated_data["assigned_at"] = datetime.date.today()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["updated_at"] = datetime.date.today()
        return super().update(instance, validated_data)
