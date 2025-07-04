from django.urls import path
from projects.views import ProjectListCreateAPIView, ProjectDetailAPIView

urlpatterns = [
    path("", ProjectListCreateAPIView.as_view(), name="project-list-create"),
    path("<int:id>", ProjectDetailAPIView.as_view(), name="project-detail"),
]
