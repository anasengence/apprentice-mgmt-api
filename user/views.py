from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Apprentice, Mentor, Trainer
from .serializers import (
    ApprenticeReadSerializer,
    ApprenticeWriteSerializer,
    MentorReadSerializer,
    MentorWriteSerializer,
    TrainerReadSerializer,
    TrainerWriteSerializer,
)
from .permissions import (
    IsTrainer,
    IsApprenticeOrTrainer,
    IsMentorOrTrainer,
    IsTrainerOrAdmin,
)
from drf_yasg.utils import swagger_auto_schema


# ───────────────────────────────────
# 1. APPRENTICE VIEWS
# ───────────────────────────────────


class ApprenticeListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTrainer]

    @swagger_auto_schema(
        operation_description="List all apprentices or create a new apprentice (Trainer only).",
        responses={
            200: ApprenticeReadSerializer(many=True),
            201: ApprenticeWriteSerializer(),
            400: "Bad Request",
        },
    )
    def get(self, request):
        apprentices = Apprentice.objects.all()
        serializer = ApprenticeReadSerializer(apprentices, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new apprentice (Trainer only).",
        responses={201: ApprenticeWriteSerializer(), 400: "Bad Request"},
        request_body=ApprenticeWriteSerializer,
    )
    def post(self, request):
        serializer = ApprenticeWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApprenticeDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsApprenticeOrTrainer]

    def get_object(self, id):
        try:
            if self.request.user.is_trainer:
                return Apprentice.objects.get(user_id=id)
            elif self.request.user.is_apprentice:
                if str(self.request.user.id) == str(id):
                    return self.request.user.apprentice_profile
                return Response(status=status.HTTP_403_FORBIDDEN)
        except (Apprentice.DoesNotExist, ValueError):
            return None

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a specific apprentice (Trainer only).",
        responses={
            200: ApprenticeReadSerializer(),
            201: ApprenticeWriteSerializer(),
            400: "Bad Request",
        },
    )
    def get(self, request, id):
        apprentice = self.get_object(id)
        if not apprentice:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif isinstance(apprentice, Response):
            return apprentice
        serializer = ApprenticeReadSerializer(apprentice)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a specific apprentice (Trainer only).",
        responses={
            200: ApprenticeReadSerializer(),
            201: ApprenticeWriteSerializer(),
            400: "Bad Request",
        },
        request_body=ApprenticeWriteSerializer,
    )
    def put(self, request, id):
        apprentice = self.get_object(id)
        if not apprentice:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif isinstance(apprentice, Response):
            return apprentice
        serializer = ApprenticeWriteSerializer(
            apprentice, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific apprentice (Trainer only).",
        responses={
            200: ApprenticeReadSerializer(),
            201: ApprenticeWriteSerializer(),
            400: "Bad Request",
        },
        request_body=ApprenticeWriteSerializer,
    )
    def delete(self, request, id):
        apprentice = self.get_object(id)
        if not apprentice:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif isinstance(apprentice, Response):
            return apprentice
        apprentice.user.delete()  # Also deletes associated User
        return Response(status=status.HTTP_204_NO_CONTENT)


# ───────────────────────────────────
# 2. MENTOR VIEWS
# ───────────────────────────────────


class MentorListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTrainer]

    @swagger_auto_schema(
        operation_description="List all mentors or create a new mentor (Trainer only).",
        responses={
            200: MentorReadSerializer(many=True),
            201: MentorWriteSerializer(),
            400: "Bad Request",
        },
    )
    def get(self, request):
        # import pdb; pdb.set_trace()
        mentors = Mentor.objects.all()
        serializer = MentorReadSerializer(mentors, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new mentor (Trainer only).",
        responses={201: MentorWriteSerializer(), 400: "Bad Request"},
        request_body=MentorWriteSerializer,
    )
    def post(self, request):
        serializer = MentorWriteSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MentorDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsMentorOrTrainer]

    def get_object(self, id):
        try:
            if self.request.user.is_trainer:
                mentor = Mentor.objects.get(user_id=id)
                return mentor
            elif self.request.user.is_mentor:
                if str(self.request.user.id) == str(id):
                    return Mentor.objects.get(user_id=self.request.user.id)
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Mentor.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a specific mentor (Trainer only).",
        responses={
            200: MentorReadSerializer(),
            201: MentorWriteSerializer(),
            400: "Bad Request",
        },
    )
    def get(self, request, id):
        mentor = self.get_object(id)
        if not mentor:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MentorReadSerializer(mentor)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a specific mentor (Trainer only).",
        responses={
            200: MentorReadSerializer(),
            201: MentorWriteSerializer(),
            400: "Bad Request",
        },
        request_body=MentorWriteSerializer,
    )
    def put(self, request, id):
        mentor = self.get_object(id)
        if not mentor:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MentorWriteSerializer(mentor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific mentor (Trainer only).",
        responses={
            200: MentorReadSerializer(),
            201: MentorWriteSerializer(),
            400: "Bad Request",
        },
        request_body=MentorWriteSerializer,
    )
    def delete(self, request, id):
        mentor = self.get_object(id)
        if not mentor:
            return Response(status=status.HTTP_404_NOT_FOUND)
        mentor.user.delete()  # Also deletes associated User
        return Response(status=status.HTTP_204_NO_CONTENT)


# ───────────────────────────────────
# 3. TRAINER VIEWS
# ───────────────────────────────────


class TrainerListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTrainerOrAdmin]

    @swagger_auto_schema(
        operation_description="List all trainers or create a new trainer (Trainer only).",
        responses={
            200: TrainerReadSerializer(many=True),
            201: TrainerWriteSerializer(),
            400: "Bad Request",
        },
    )
    def get(self, request):
        trainers = Trainer.objects.all()
        serializer = TrainerReadSerializer(trainers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new trainer (Trainer only).",
        responses={201: TrainerWriteSerializer(), 400: "Bad Request"},
        request_body=TrainerWriteSerializer,
    )
    def post(self, request):
        serializer = TrainerWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrainerDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTrainer]

    def get_object(self, id):
        try:
            return Trainer.objects.get(user_id=id)
        except Trainer.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a specific trainer (Trainer only).",
        responses={
            200: TrainerReadSerializer(),
            201: TrainerWriteSerializer(),
            400: "Bad Request",
        },
    )
    def get(self, request, id):
        trainer = self.get_object(id)
        if not trainer:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TrainerReadSerializer(trainer)

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a specific trainer (Trainer only).",
        responses={
            200: TrainerReadSerializer(),
            201: TrainerWriteSerializer(),
            400: "Bad Request",
        },
        request_body=TrainerWriteSerializer,
    )
    def put(self, request, id):
        trainer = self.get_object(id)
        if not trainer:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TrainerWriteSerializer(trainer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific trainer (Trainer only).",
        responses={
            200: TrainerReadSerializer(),
            201: TrainerWriteSerializer(),
            400: "Bad Request",
        },
        request_body=TrainerWriteSerializer,
    )
    def delete(self, request, id):
        trainer = self.get_object(id)
        if not trainer:
            return Response(status=status.HTTP_404_NOT_FOUND)
        trainer.user.delete()  # Also deletes associated User
        return Response(status=status.HTTP_204_NO_CONTENT)
