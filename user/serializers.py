from rest_framework import serializers
from .models import User, Trainer, Mentor, Apprentice


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
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
        ]

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class TrainerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trainer
        fields = [
            "id",
            "user",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["is_trainer"] = True
        user = User.objects.create(**user_data)
        trainer = Trainer.objects.create(user=user)
        return trainer

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        instance.save()
        return instance


class MentorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Mentor
        fields = [
            "id",
            "user",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["is_mentor"] = True
        if user_data.get("is_external"):
            user_data["is_external"] = True
        user = User.objects.create(**user_data)
        mentor = Mentor.objects.create(user=user)
        return mentor

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        instance.save()
        return instance


class ApprenticeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Apprentice
        fields = [
            "id",
            "user",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["is_apprentice"] = True
        user = User.objects.create(**user_data)
        apprentice = Apprentice.objects.create(user=user)
        return apprentice

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        instance.save()
        return instance
