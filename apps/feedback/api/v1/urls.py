from django.urls import path

from .views import (
    FeedbackListCreateView,
    ProjectFeedbackView,
    FeedbackDetailView,
    ApprenticeFeedbackView,
)

urlpatterns = [
    path("", FeedbackListCreateView.as_view(), name="feedback-list-create"),
    path("<uuid:feedback_id>/", FeedbackDetailView.as_view(), name="feedback-detail"),
    path("project/<uuid:project_id>/", ProjectFeedbackView.as_view(), name="project-feedback"),
    path("apprentice/<uuid:apprentice_id>/", ApprenticeFeedbackView.as_view(), name="apprentice-feedback"),
]
