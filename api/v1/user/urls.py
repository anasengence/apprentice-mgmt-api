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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


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

schema_view = get_schema_view(
    openapi.Info(
        title="Apprentice Management API",
        default_version="v1",
        description="API for managing apprentices, mentors, and trainers",
    ),
    public=True,
    patterns=urlpatterns,  # ← safest: lock it to these patterns
)

# finally expose the docs
urlpatterns += [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
