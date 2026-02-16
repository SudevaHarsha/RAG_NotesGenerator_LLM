from django.urls import path
from .views import CourseCreateView, CourseListView

urlpatterns = [
    path("create/", CourseCreateView.as_view(), name="create-course"),
    path("list/", CourseListView.as_view(), name="list-courses"),
]
