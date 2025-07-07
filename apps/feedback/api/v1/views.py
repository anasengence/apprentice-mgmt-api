# feedback/views.py
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.feedback.models import Feedback
from .serializers import FeedbackReadSerializer, FeedbackWriteSerializer
from apps.core.permissions import IsMentor, IsMentorOrApprentice
from drf_yasg.utils import swagger_auto_schema

# ─────────────────────────────────────────────
# 1. Feedback List + Create  (Mentors only)
# ─────────────────────────────────────────────
class FeedbackListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMentor]

    @swagger_auto_schema(
        responses={200: FeedbackReadSerializer(many=True)},
    )
    def get(self, request):
        qs = Feedback.objects.filter(mentor=request.user.mentor_profile).select_related(
            "mentor__user", "apprentice__user", "project"
        )
        return Response(FeedbackReadSerializer(qs, many=True).data)

    @swagger_auto_schema(
        request_body=FeedbackWriteSerializer,
        responses={201: FeedbackReadSerializer},
    )
    def post(self, request):
        ser = FeedbackWriteSerializer(data=request.data, context={"request": request})
        if ser.is_valid():
            ser.save()  # mentor, apprentice, project IDs must be included
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────────
# 2. Feedback Detail (mentor update, apprentice view)
# ─────────────────────────────────────────────
class FeedbackDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMentorOrApprentice]

    def get_object(self, feedback_id):
        obj = get_object_or_404(Feedback, id=feedback_id)
        self.check_object_permissions(self.request, obj)
        return obj

    @swagger_auto_schema(
        responses={200: FeedbackReadSerializer},
    )
    def get(self, request, feedback_id):
        return Response(FeedbackReadSerializer(self.get_object(feedback_id)).data)

    @swagger_auto_schema(
        request_body=FeedbackWriteSerializer,
        responses={200: FeedbackReadSerializer},
    )
    def put(self, request, feedback_id):
        feedback = self.get_object(feedback_id)
        ser = FeedbackWriteSerializer(feedback, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(FeedbackReadSerializer(feedback).data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────────
# 3. Apprentice Feedback (all feedback about apprentice)
# ─────────────────────────────────────────────
class ApprenticeFeedbackView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMentorOrApprentice]

    @swagger_auto_schema(
        responses={200: FeedbackReadSerializer(many=True)},
    )
    def get(self, request, apprentice_id):
        qs = Feedback.objects.filter(apprentice_id=apprentice_id).select_related(
            "mentor__user", "project"
        )
        # object‑level perms checked row by row
        result = [
            FeedbackReadSerializer(fb).data
            for fb in qs
            if self.check_object_permissions(request, fb) is None
        ]
        return Response(result)


# ─────────────────────────────────────────────
# 4. Project Feedback (all feedback for a project)
# ─────────────────────────────────────────────
class ProjectFeedbackView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMentor]

    @swagger_auto_schema(
        responses={200: FeedbackReadSerializer(many=True)},
    )
    def get(self, request, project_id):
        qs = Feedback.objects.filter(project_id=project_id).select_related(
            "mentor__user", "apprentice__user"
        )
        return Response(FeedbackReadSerializer(qs, many=True).data)
