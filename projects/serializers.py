from rest_framework import serializers
from .models import Project
import datetime


class ProjectReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "name", "description", "start_date", "end_date", "trainer", "created_at", "updated_at", "is_external")


class ProjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "name", "description", "start_date", "end_date", "trainer", "is_external")
    
    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.trainer = validated_data.get("trainer", instance.trainer)
        instance.is_external = validated_data.get("is_external", instance.is_external)
        instance.updated_at = datetime.datetime.now()
        instance.save()
        return instance