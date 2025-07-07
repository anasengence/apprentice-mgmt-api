from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/user/", include("apps.user.api.v1.urls"), name="v1"),
    path("api/v1/tasks/", include("apps.tasks.api.v1.urls"), name="v1"),
    path("api/v1/requests/", include("apps.request.api.v1.urls"), name="v1"),
    path("api/v1/projects/", include("apps.projects.api.v1.urls"), name="v1"),
    path("api/v1/feedback/", include("apps.feedback.api.v1.urls"), name="v1"),
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