# apps/requests/views.py

from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.request.models import (
    ProjectJoinRequest,
    ProjectLeaveRequest,
    RotationChangeRequest,
    MentorLeaveRequest,
    ApprenticeRemovalRequest,
)
from .serializers import (
    ProjectJoinRequestSerializer,
    ProjectLeaveRequestSerializer,
    RotationChangeRequestSerializer,
    MentorLeaveRequestSerializer,
    ApprenticeRemovalRequestSerializer,
)
from apps.core.permissions import IsTrainerOrAdmin, IsApprentice, IsMentor
from drf_yasg.utils import swagger_auto_schema


# ─────────────────────────────────────────────────────────
# General Request Management Views
# ─────────────────────────────────────────────────────────


class RequestListView(APIView):
    """List *all* requests (Trainer only)."""

    permission_classes = [permissions.IsAuthenticated, IsTrainerOrAdmin]

    @swagger_auto_schema(
        operation_summary="List all requests",
        operation_description="List all requests (Trainer only)",
    )
    def get(self, request):
        all_reqs = (
            list(ProjectJoinRequest.objects.all())
            + list(ProjectLeaveRequest.objects.all())
            + list(RotationChangeRequest.objects.all())
            + list(MentorLeaveRequest.objects.all())
            + list(ApprenticeRemovalRequest.objects.all())
        )
        # serialize each by type
        data = []
        for req in all_reqs:
            serializer = {
                ProjectJoinRequest: ProjectJoinRequestSerializer,
                ProjectLeaveRequest: ProjectLeaveRequestSerializer,
                RotationChangeRequest: RotationChangeRequestSerializer,
                MentorLeaveRequest: MentorLeaveRequestSerializer,
                ApprenticeRemovalRequest: ApprenticeRemovalRequestSerializer,
            }[req.__class__](req).data
            data.append(serializer)
        return Response(data)


class RequestApprovalView(APIView):
    """Approve or reject a request (Trainer only)."""

    permission_classes = [permissions.IsAuthenticated, IsTrainerOrAdmin]

    @swagger_auto_schema(
        operation_summary="Approve or reject a request",
        operation_description="Approve or reject a request (Trainer only)",
    )
    def post(self, request, req_type, req_id):
        model = {
            "join": ProjectJoinRequest,
            "leave": ProjectLeaveRequest,
            "rotation": RotationChangeRequest,
            "mentor_leave": MentorLeaveRequest,
            "remove_apprentice": ApprenticeRemovalRequest,
        }[req_type]
        req = get_object_or_404(model, id=req_id)
        action = request.data.get("status")
        if action not in dict(model.STATUS_CHOICES):
            return Response(
                {"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST
            )
        req.status = action
        req.reviewed_by = request.user
        req.admin_notes = request.data.get("admin_notes", "")
        req.save()
        ser = {
            ProjectJoinRequest: ProjectJoinRequestSerializer,
            ProjectLeaveRequest: ProjectLeaveRequestSerializer,
            RotationChangeRequest: RotationChangeRequestSerializer,
            MentorLeaveRequest: MentorLeaveRequestSerializer,
            ApprenticeRemovalRequest: ApprenticeRemovalRequestSerializer,
        }[model](req)
        return Response(ser.data)


class MyRequestsView(APIView):
    """Get all requests created by the current user."""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get all requests created by the current user",
        operation_description="Get all requests created by the current user",
    )
    def get(self, request):
        user = request.user
        qsets = [
            ProjectJoinRequest.objects.filter(requester=user),
            ProjectLeaveRequest.objects.filter(requester=user),
            RotationChangeRequest.objects.filter(requester=user),
            MentorLeaveRequest.objects.filter(requester=user),
            ApprenticeRemovalRequest.objects.filter(requester=user),
        ]
        data = []
        for qs, serializer_class in zip(
            qsets,
            [
                ProjectJoinRequestSerializer,
                ProjectLeaveRequestSerializer,
                RotationChangeRequestSerializer,
                MentorLeaveRequestSerializer,
                ApprenticeRemovalRequestSerializer,
            ],
        ):
            data.extend(serializer_class(qs, many=True).data)
        return Response(data)


class RequestStatusUpdateView(APIView):
    """Trainer updates status directly (duplicate of approval)."""

    permission_classes = [permissions.IsAuthenticated, IsTrainerOrAdmin]

    @swagger_auto_schema(
        operation_summary="Update request status",
        operation_description="Update request status (Trainer only)",
    )
    def patch(self, request, req_type, req_id):
        return RequestApprovalView().post(request, req_type, req_id)


# ─────────────────────────────────────────────────────────
# Specific Request Views (creation endpoints)
# ─────────────────────────────────────────────────────────


class ProjectJoinRequestView(APIView):
    """Apprentice requests to join a project."""

    permission_classes = [permissions.IsAuthenticated, IsApprentice]

    @swagger_auto_schema(
        operation_summary="Create a project join request",
        operation_description="Create a project join request (Apprentice only)",
    )
    def post(self, request):
        ser = ProjectJoinRequestSerializer(data=request.data)
        if ser.is_valid():
            ser.save(requester=request.user, status="pending")
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectLeaveRequestView(APIView):
    """Apprentice or Mentor requests to leave a project."""

    permission_classes = [permissions.IsAuthenticated, IsApprentice]

    @swagger_auto_schema(
        operation_summary="Create a project leave request",
        operation_description="Create a project leave request (Apprentice only)",
    )
    def post(self, request):
        ser = ProjectLeaveRequestSerializer(data=request.data)
        if ser.is_valid():
            ser.save(requester=request.user, status="pending")
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class RotationChangeRequestView(APIView):
    """Apprentice requests a rotation change."""

    permission_classes = [permissions.IsAuthenticated, IsApprentice]

    @swagger_auto_schema(
        operation_summary="Create a rotation change request",
        operation_description="Create a rotation change request (Apprentice only)",
    )
    def post(self, request):
        ser = RotationChangeRequestSerializer(data=request.data)
        if ser.is_valid():
            ser.save(requester=request.user, status="pending")
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class MentorLeaveRequestView(APIView):
    """Mentor requests to leave a project."""

    permission_classes = [permissions.IsAuthenticated, IsMentor]

    @swagger_auto_schema(
        operation_summary="Create a mentor leave request",
        operation_description="Create a mentor leave request (Mentor only)",
    )
    def post(self, request):
        ser = MentorLeaveRequestSerializer(data=request.data)
        if ser.is_valid():
            ser.save(requester=request.user, status="pending")
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ApprenticeRemovalRequestView(APIView):
    """Mentor requests removal of an apprentice from a project."""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create an apprentice removal request",
        operation_description="Create an apprentice removal request (Mentor only)",
        request_body=ApprenticeRemovalRequestSerializer,
        responses={
            201: ApprenticeRemovalRequestSerializer,
            400: "Bad Request",
            403: "Forbidden",
        },
    )
    def post(self, request):
        # Ensure the requesting user is a mentor
        if not hasattr(request.user, "mentor_profile"):
            return Response(
                {"detail": "Only mentors can create removal requests."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ApprenticeRemovalRequestSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            # Automatically set the mentor to the current user's mentor profile
            validated_data = serializer.validated_data
            validated_data["mentor"] = request.user.mentor_profile

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────────────────────
# Request Processing & Notifications
# ─────────────────────────────────────────────────────────


class PendingRequestsView(APIView):
    """Trainer views all pending requests."""

    permission_classes = [permissions.IsAuthenticated, IsTrainerOrAdmin]

    @swagger_auto_schema(
        operation_summary="View all pending requests",
        operation_description="View all pending requests (Trainer only)",
    )
    def get(self, request):
        q = (
            ProjectJoinRequest.objects.filter(status="pending")
            | ProjectLeaveRequest.objects.filter(status="pending")
            | RotationChangeRequest.objects.filter(status="pending")
            | MentorLeaveRequest.objects.filter(status="pending")
            | ApprenticeRemovalRequest.objects.filter(status="pending")
        )
        # serialize as in RequestListView
        data = []
        for req in q:
            serializer = {
                ProjectJoinRequest: ProjectJoinRequestSerializer,
                ProjectLeaveRequest: ProjectLeaveRequestSerializer,
                RotationChangeRequest: RotationChangeRequestSerializer,
                MentorLeaveRequest: MentorLeaveRequestSerializer,
                ApprenticeRemovalRequest: ApprenticeRemovalRequestSerializer,
            }[req.__class__](req).data
            data.append(serializer)
        return Response(data)


class ProcessedRequestsView(APIView):
    """Trainer views all processed (approved/rejected) requests."""

    permission_classes = [permissions.IsAuthenticated, IsTrainerOrAdmin]

    @swagger_auto_schema(
        operation_summary="View all processed requests",
        operation_description="View all processed requests (Trainer only)",
    )
    def get(self, request):
        # similar to PendingRequestsView but filter status != 'pending'
        q = (
            ProjectJoinRequest.objects.filter(status__in=["approved", "rejected"])
            | ProjectLeaveRequest.objects.filter(status__in=["approved", "rejected"])
            | RotationChangeRequest.objects.filter(status__in=["approved", "rejected"])
            | MentorLeaveRequest.objects.filter(status__in=["approved", "rejected"])
            | ApprenticeRemovalRequest.objects.filter(
                status__in=["approved", "rejected"]
            )
        )
        # serialize as in RequestListView
        data = []
        for req in q:
            serializer = {
                ProjectJoinRequest: ProjectJoinRequestSerializer,
                ProjectLeaveRequest: ProjectLeaveRequestSerializer,
                RotationChangeRequest: RotationChangeRequestSerializer,
                MentorLeaveRequest: MentorLeaveRequestSerializer,
                ApprenticeRemovalRequest: ApprenticeRemovalRequestSerializer,
            }[req.__class__](req).data
            data.append(serializer)
        return Response(data)


class RequestNotificationsView(APIView):
    """Get all requests where current user is the approver or requester."""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="View all notifications",
        operation_description="View all notifications (Trainer only)",
    )
    def get(self, request):
        # combine requests where requester==user or reviewed_by==user
        q = (
            ProjectJoinRequest.objects.filter(requester=request.user)
            | ProjectLeaveRequest.objects.filter(requester=request.user)
            | RotationChangeRequest.objects.filter(requester=request.user)
            | MentorLeaveRequest.objects.filter(requester=request.user)
            | ApprenticeRemovalRequest.objects.filter(requester=request.user)
            | ProjectJoinRequest.objects.filter(reviewed_by=request.user)
            | ProjectLeaveRequest.objects.filter(reviewed_by=request.user)
            | RotationChangeRequest.objects.filter(reviewed_by=request.user)
            | MentorLeaveRequest.objects.filter(reviewed_by=request.user)
            | ApprenticeRemovalRequest.objects.filter(reviewed_by=request.user)
        )
        # serialize as in RequestListView
        data = []
        for req in q:
            serializer = {
                ProjectJoinRequest: ProjectJoinRequestSerializer,
                ProjectLeaveRequest: ProjectLeaveRequestSerializer,
                RotationChangeRequest: RotationChangeRequestSerializer,
                MentorLeaveRequest: MentorLeaveRequestSerializer,
                ApprenticeRemovalRequest: ApprenticeRemovalRequestSerializer,
            }[req.__class__](req).data
            data.append(serializer)
        return Response(data)
