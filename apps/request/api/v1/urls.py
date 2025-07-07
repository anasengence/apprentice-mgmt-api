from django.urls import path
from .views import (
    RequestListView,
    RequestApprovalView,
    # MyRequestsView,
    ProjectJoinRequestView,
    ProjectLeaveRequestView,
    RotationChangeRequestView,
    MentorLeaveRequestView,
    ApprenticeRemovalRequestView,
    PendingRequestsView,
    ProcessedRequestsView,
    # RequestNotificationsView,
)

urlpatterns = [
    path("", RequestListView.as_view()),
    path("<str:req_type>/<uuid:req_id>/approve/", RequestApprovalView.as_view()),
    # path("mine/", MyRequestsView.as_view()),
    path("project/join/", ProjectJoinRequestView.as_view()),
    path("project/leave/", ProjectLeaveRequestView.as_view()),
    path("rotation/change/", RotationChangeRequestView.as_view()),
    path("mentor/leave/", MentorLeaveRequestView.as_view()),
    path("apprentice/removal/", ApprenticeRemovalRequestView.as_view()),
    path("pending/", PendingRequestsView.as_view()),
    path("processed/", ProcessedRequestsView.as_view()),
    # path("notifications/", RequestNotificationsView.as_view()),
]
