"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/user/", include("apps.user.api.v1.urls"), name="v1"),
    path("api/v1/projects/", include("apps.projects.api.v1.urls"), name="v1"),
    path("api/v1/tasks/", include("apps.tasks.api.v1.urls"), name="v1"),
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