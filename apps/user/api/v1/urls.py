from django.urls import path
from .views import (
    ApprenticeListCreateAPIView,
    ApprenticeDetailAPIView,
    MentorListCreateAPIView,
    MentorDetailAPIView,
    TrainerListCreateAPIView,
    TrainerDetailAPIView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("apprentices/", ApprenticeListCreateAPIView.as_view(), name="apprentice-list-create"),
    path("apprentices/<int:id>/", ApprenticeDetailAPIView.as_view(), name="apprentice-detail"),
    path("mentors/", MentorListCreateAPIView.as_view(), name="mentor-list-create"),
    path("mentors/<int:id>/", MentorDetailAPIView.as_view(), name="mentor-detail"),
    path("trainers/", TrainerListCreateAPIView.as_view(), name="trainer-list-create"),
    path("trainers/<int:id>/", TrainerDetailAPIView.as_view(), name="trainer-detail"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
