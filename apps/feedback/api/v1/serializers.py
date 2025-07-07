# feedback/serializers.py
from rest_framework import serializers
from apps.feedback.models import Feedback
# from apps.user.api.v1.serializers import MentorReadSerializer, ApprenticeReadSerializer
# from apps.projects.api.v1.serializers import ProjectReadSerializer


class FeedbackReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = "__all__"


class FeedbackWriteSerializer(serializers.ModelSerializer):
    """Used for POST ‑ mentor supplies IDs, not nested objects."""

    class Meta:
        model = Feedback
        fields = [
            "description",
            "apprentice",
            "project",
            "satisfied",
        ]
    def create(self, validated_data):
        validated_data['mentor'] = self.context['request'].user.mentor_profile
        return Feedback.objects.create(**validated_data)
