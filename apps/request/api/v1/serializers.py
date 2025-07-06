from rest_framework import serializers
from apps.request.models import ProjectJoinRequest, ProjectLeaveRequest, RotationChangeRequest, MentorLeaveRequest, ApprenticeRemovalRequest
from apps.user.models import Mentor

class ProjectJoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectJoinRequest
        fields = '__all__'


class ProjectLeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLeaveRequest
        fields = '__all__'


class RotationChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RotationChangeRequest
        fields = '__all__'


class MentorLeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorLeaveRequest
        fields = '__all__'


class ApprenticeRemovalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprenticeRemovalRequest
        fields = ['id', 'mentor', 'apprentice', 'project', 'reason', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

    def validate(self, data):
        mentor = data.get('mentor')
        apprentice = data.get('apprentice')
        project = data.get('project')

        # Check if mentor is assigned to this apprentice on this project
        if not Mentor.objects.filter(
            user=mentor.user,
            project=project,
            apprentices=apprentice
        ).exists():
            raise serializers.ValidationError(
                "You can only request removal for apprentices assigned to you on this project."
            )

        return data