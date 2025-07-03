from django.urls import path
from user.views import (
    UserListCreateAPIView,
    UserDetailAPIView,
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
    # TOKENS
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # login
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # refresh token
    # USERS
    path("", UserListCreateAPIView.as_view(), name="user-list-create"),
    path("<uuid:id>/", UserDetailAPIView.as_view(), name="user-detail"),
    path(
        "apprentices/",
        ApprenticeListCreateAPIView.as_view(),
        name="apprentice-list-create",
    ),
    path(
        "apprentices/<uuid:id>/",
        ApprenticeDetailAPIView.as_view(),
        name="apprentice-detail",
    ),
    path("mentors/", MentorListCreateAPIView.as_view(), name="mentor-list-create"),
    path("mentors/<uuid:id>/", MentorDetailAPIView.as_view(), name="mentor-detail"),
    path("trainers/", TrainerListCreateAPIView.as_view(), name="trainer-list-create"),
    path("trainers/<uuid:id>/", TrainerDetailAPIView.as_view(), name="trainer-detail"),
]
