from django.urls import path

from .views import CourseDetailView, CourseListView, LessonDetailView

urlpatterns = [
    path("courses/", CourseListView.as_view(), name="course-list"),
    path("courses/<slug:slug>/", CourseDetailView.as_view(), name="course-detail"),
    path(
        "courses/<slug:course_slug>/lessons/<slug:lesson_slug>/",
        LessonDetailView.as_view(),
        name="lesson-detail",
    ),
]
