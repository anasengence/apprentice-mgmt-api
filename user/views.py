from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import User, Apprentice, Mentor, Trainer
from .serializers import UserSerializer, ApprenticeSerializer, MentorSerializer, TrainerSerializer
from .permissions import IsTrainer, IsApprenticeOrTrainer, IsMentorOrTrainer
from drf_yasg.utils import swagger_auto_schema

class UserListCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="List all users or create a new user (Trainer only).",
        responses={200: UserSerializer(many=True), 201: UserSerializer(), 400: "Bad Request"},
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    
    @swagger_auto_schema(
        operation_description="Create a new user (Trainer only).",
        responses={201: UserSerializer(), 400: "Bad Request"},
        request_body=UserSerializer
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("User not found")
    
    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a specific user (Trainer only).",
        responses={200: UserSerializer(), 201: UserSerializer(), 400: "Bad Request"},
    )
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Update a specific user (Trainer only).",
        responses={200: UserSerializer(), 201: UserSerializer(), 400: "Bad Request"},
        request_body=UserSerializer
    )
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete a specific user (Trainer only).",
        responses={200: UserSerializer(), 201: UserSerializer(), 400: "Bad Request"},
        request_body=UserSerializer
    )
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ApprenticeListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTrainer]
    @swagger_auto_schema(
        operation_description="List all apprentices or create a new apprentice (Trainer only).",
        responses={200: ApprenticeSerializer(many=True), 201: ApprenticeSerializer(), 400: "Bad Request"},
    )
    def get(self, request):
        apprentices = Apprentice.objects.all()
        serializer = ApprenticeSerializer(apprentices, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Create a new apprentice (Trainer only).",
        responses={201: ApprenticeSerializer(), 400: "Bad Request"},
        request_body=ApprenticeSerializer
    )
    def post(self, request):
        serializer = ApprenticeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApprenticeDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsApprenticeOrTrainer]

    def get_object(self, id):
        try:
            return Apprentice.objects.get(id=id)
        except Apprentice.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a specific apprentice (Trainer only).",
        responses={200: ApprenticeSerializer(), 201: ApprenticeSerializer(), 400: "Bad Request"},
    )   

    def get(self, request, id):
        apprentice = self.get_object(id)
        if not apprentice:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ApprenticeSerializer(apprentice)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a specific apprentice (Trainer only).",
        responses={200: ApprenticeSerializer(), 201: ApprenticeSerializer(), 400: "Bad Request"},
        request_body=ApprenticeSerializer
    )
    def put(self, request, id):
        apprentice = self.get_object(id)
        if not apprentice:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ApprenticeSerializer(apprentice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific apprentice (Trainer only).",
        responses={200: ApprenticeSerializer(), 201: ApprenticeSerializer(), 400: "Bad Request"},
        request_body=ApprenticeSerializer
    )
    def delete(self, request, id):
        apprentice = self.get_object(id)
        if not apprentice:
            return Response(status=status.HTTP_404_NOT_FOUND)
        apprentice.user.delete()  # Also deletes associated User
        return Response(status=status.HTTP_204_NO_CONTENT)

class MentorListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTrainer]
    @swagger_auto_schema(
        operation_description="List all mentors or create a new mentor (Trainer only).",
        responses={200: MentorSerializer(many=True), 201: MentorSerializer(), 400: "Bad Request"},
    )
    def get(self, request):
        mentors = Mentor.objects.all()
        serializer = MentorSerializer(mentors, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new mentor (Trainer only).",
        responses={201: MentorSerializer(), 400: "Bad Request"},
        request_body=MentorSerializer
    )
    def post(self, request):
        serializer = MentorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MentorDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsMentorOrTrainer]

    def get_object(self, id):
        try:
            return Mentor.objects.get(id=id)
        except Mentor.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a specific mentor (Trainer only).",
        responses={200: MentorSerializer(), 201: MentorSerializer(), 400: "Bad Request"},
    )
    def get(self, request, id):
        mentor = self.get_object(id)
        if not mentor:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MentorSerializer(mentor)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a specific mentor (Trainer only).",
        responses={200: MentorSerializer(), 201: MentorSerializer(), 400: "Bad Request"},
        request_body=MentorSerializer
    )
    def put(self, request, id):
        mentor = self.get_object(id)
        if not mentor:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MentorSerializer(mentor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific mentor (Trainer only).",
        responses={200: MentorSerializer(), 201: MentorSerializer(), 400: "Bad Request"},
        request_body=MentorSerializer
    )
    def delete(self, request, id):
        mentor = self.get_object(id)
        if not mentor:
            return Response(status=status.HTTP_404_NOT_FOUND)
        mentor.user.delete()  # Also deletes associated User
        return Response(status=status.HTTP_204_NO_CONTENT)

class TrainerListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTrainer]
    @swagger_auto_schema(
        operation_description="List all trainers or create a new trainer (Trainer only).",
        responses={200: TrainerSerializer(many=True), 201: TrainerSerializer(), 400: "Bad Request"},
    )
    def get(self, request):
        trainers = Trainer.objects.all()
        serializer = TrainerSerializer(trainers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new trainer (Trainer only).",
        responses={201: TrainerSerializer(), 400: "Bad Request"},
        request_body=TrainerSerializer
    )
    def post(self, request):
        serializer = TrainerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TrainerDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTrainer]
    def get_object(self, id):
        try:
            return Trainer.objects.get(id=id)
        except Trainer.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a specific trainer (Trainer only).",
        responses={200: TrainerSerializer(), 201: TrainerSerializer(), 400: "Bad Request"},
    )
    def get(self, request, id):
        trainer = self.get_object(id)
        if not trainer:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TrainerSerializer(trainer)

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a specific trainer (Trainer only).",
        responses={200: TrainerSerializer(), 201: TrainerSerializer(), 400: "Bad Request"},
        request_body=TrainerSerializer
    )
    def put(self, request, id):
        trainer = self.get_object(id)
        if not trainer:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TrainerSerializer(trainer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific trainer (Trainer only).",
        responses={200: TrainerSerializer(), 201: TrainerSerializer(), 400: "Bad Request"},
        request_body=TrainerSerializer
    )
    def delete(self, request, id):
        trainer = self.get_object(id)
        if not trainer:
            return Response(status=status.HTTP_404_NOT_FOUND)
        trainer.user.delete()  # Also deletes associated User
        return Response(status=status.HTTP_204_NO_CONTENT)
