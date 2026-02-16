from django.urls import path
from .views import SlideRAGAPIView, TaskStatusAPIView

urlpatterns = [
    path("generate/", SlideRAGAPIView.as_view(), name="slide-rag-generate"),
    path("task-status/<str:task_id>/", TaskStatusAPIView.as_view(), name="task-status"),
]
