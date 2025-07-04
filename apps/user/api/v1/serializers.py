# serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.user.models import Trainer, Mentor, Apprentice
from apps.projects.models import Project

User = get_user_model()

# ───────────────────────────────────
# 1. USER SERIALIZERS
# ───────────────────────────────────


class UserReadSerializer(serializers.ModelSerializer):
    """Returned in all GET responses – never accepted as input."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_trainer",
            "is_mentor",
            "is_apprentice",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class UserWriteSerializer(serializers.ModelSerializer):
    """Used inside POST / PUT / PATCH payloads."""

    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# ───────────────────────────────────
# 2. TRAINER SERIALIZERS
# ───────────────────────────────────


class TrainerReadSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()

    class Meta:
        model = Trainer
        fields = ("user",)


class TrainerWriteSerializer(serializers.ModelSerializer):
    user = UserWriteSerializer()

    class Meta:
        model = Trainer
        fields = ("user",)

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data.update(is_trainer=True)
        user = UserWriteSerializer().create(user_data)
        return Trainer.objects.create(user=user)

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            UserWriteSerializer().update(instance.user, user_data)
        return instance


# ───────────────────────────────────
# 3. MENTOR SERIALIZERS
# ───────────────────────────────────


class MentorReadSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()
    trainer = serializers.PrimaryKeyRelatedField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    apprentice = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Mentor
        fields = ("user", "trainer", "is_external", "project", "apprentice")


class MentorWriteSerializer(serializers.ModelSerializer):
    user = UserWriteSerializer()
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Mentor
        fields = ("user", "is_external", "project")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data.update(is_mentor=True)
        user = UserWriteSerializer().create(user_data)

        trainer = self.context.get("request").user.trainer_profile
        if not trainer:
            raise serializers.ValidationError(
                "Trainer must be supplied or inferred from the authenticated trainer."
            )
        project = validated_data.get("project")
        if not project:
            raise serializers.ValidationError(
                "Project must be supplied or inferred from the authenticated trainer."
            )

        return Mentor.objects.create(user=user, trainer=trainer, project=project)

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            UserWriteSerializer().update(instance.user, user_data)
        trainer = validated_data.get("trainer")
        if trainer:
            instance.trainer = trainer
        project = validated_data.get("project")
        if project:
            instance.project = project
        instance.save()
        return instance


# ───────────────────────────────────
# 4. APPRENTICE SERIALIZERS
# ───────────────────────────────────


class ApprenticeReadSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()
    trainer = serializers.PrimaryKeyRelatedField(read_only=True)
    mentor = serializers.PrimaryKeyRelatedField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Apprentice
        fields = ("user", "trainer", "mentor", "project")


class ApprenticeWriteSerializer(serializers.ModelSerializer):
    user = UserWriteSerializer()
    mentor = serializers.PrimaryKeyRelatedField(
        queryset=Mentor.objects.all(), required=False
    )
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Apprentice
        fields = ("user", "mentor", "project")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data.update(is_apprentice=True)
        user = UserWriteSerializer().create(user_data)

        trainer = self.context.get("request").user.trainer_profile
        if not trainer:
            raise serializers.ValidationError(
                "Trainer must be supplied or inferred from the authenticated trainer."
            )

        mentor = validated_data.get("mentor")
        if not mentor:
            raise serializers.ValidationError(
                "Mentor must be supplied or inferred from the authenticated trainer."
            )

        project = validated_data.get("project")
        if not project:
            raise serializers.ValidationError(
                "Project must be supplied or inferred from the authenticated trainer."
            )
        return Apprentice.objects.create(
            user=user,
            trainer=trainer,
            mentor=mentor,
            project=project,
        )

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            UserWriteSerializer().update(instance.user, user_data)
        for field in ("trainer", "mentor"):
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()
        return instance
