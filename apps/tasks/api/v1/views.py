from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskReadSerializer, TaskWriteSerializer
from apps.tasks.models import Task
from drf_yasg.utils import swagger_auto_schema


class TaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Get all tasks",
        operation_description="Get all tasks (Apprentice, Mentor, Trainer)",
        responses={200: TaskReadSerializer(many=True)}
    )
    def get(self, request):
        if request.user.is_trainer:
            tasks = Task.objects.all()
        elif request.user.is_mentor:
            tasks = Task.objects.filter(assigned_by=request.user)
        elif request.user.is_apprentice:
            tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskReadSerializer(tasks, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a task",
        operation_description="Create a task (Mentor only)",
        request_body=TaskWriteSerializer, responses={201: TaskReadSerializer}
    )
    def post(self, request):
        if request.user.is_apprentice:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = TaskWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            if self.request.user.is_apprentice:
                return Task.objects.get(pk=pk, assigned_to=self.request.user)
            elif self.request.user.is_mentor:
                return Task.objects.get(pk=pk, assigned_by=self.request.user)
            elif self.request.user.is_trainer:
                return Task.objects.get(pk=pk)
            return None
        except Task.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_summary="Get a task",
        operation_description="Get a task (Apprentice, Mentor, Trainer)",
        responses={200: TaskReadSerializer}
    )
    def get(self, request, pk):
        task = self.get_object(pk)
        if not task:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskReadSerializer(task)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update a task",
        operation_description="Update a task (Mentor only)",
        request_body=TaskWriteSerializer, responses={200: TaskReadSerializer}
    )
    def put(self, request, pk):
        task = self.get_object(pk)
        if not task:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskWriteSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a task",
        operation_description="Delete a task (Mentor only)",
        responses={204: "No Content"}
    )
    def delete(self, request, pk):
        if request.user.is_apprentice:
            return Response(status=status.HTTP_403_FORBIDDEN)
        task = self.get_object(pk)
        if not task:
            return Response(status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
