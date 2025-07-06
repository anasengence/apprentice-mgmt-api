from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.projects.models import Project
from .serializers import ProjectReadSerializer, ProjectWriteSerializer
from apps.core.permissions import IsTrainerOrAdmin
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema


class ProjectListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTrainerOrAdmin]

    @swagger_auto_schema(
        operation_summary="List all projects or create a new project",
        operation_description="List all projects or create a new project (Trainer only).",
        responses={
            200: ProjectReadSerializer(many=True),
            201: ProjectWriteSerializer(),
            400: "Bad Request",
        },
    )
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectReadSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new project",
        operation_description="Create a new project (Trainer only).",
        responses={201: ProjectWriteSerializer(), 400: "Bad Request"},
        request_body=ProjectWriteSerializer,
    )
    def post(self, request):
        serializer = ProjectWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTrainerOrAdmin]

    def get_object(self, id):
        try:
            return Project.objects.get(id=id)
        except Project.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_summary="Retrieve a specific project",
        operation_description="Retrieve a specific project (Trainer only).",
        responses={
            200: ProjectReadSerializer(),
            201: ProjectWriteSerializer(),
            400: "Bad Request",
        },
    )
    def get(self, request, id):
        project = self.get_object(id)
        if not project:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectReadSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a specific project",
        operation_description="Update a specific project (Trainer only).",
        responses={
            200: ProjectReadSerializer(),
            201: ProjectWriteSerializer(),
            400: "Bad Request",
        },
        request_body=ProjectWriteSerializer,
    )
    def put(self, request, id):
        project = self.get_object(id)
        if not project:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectWriteSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a specific project",
        operation_description="Delete a specific project (Trainer only).",
        responses={
            200: ProjectReadSerializer(),
            201: ProjectWriteSerializer(),
            400: "Bad Request",
        },
        request_body=ProjectWriteSerializer,
    )
    def delete(self, request, id):
        project = self.get_object(id)
        if not project:
            return Response(status=status.HTTP_404_NOT_FOUND)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
