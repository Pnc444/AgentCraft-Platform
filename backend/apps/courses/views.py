from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from apps.learning.models import Progress

from .models import Course, Lesson
from .serializers import CourseDetailSerializer, LessonDetailSerializer


def progress_map(user, lessons):
    """Map of lesson_id -> progress status for the given user."""
    return dict(
        Progress.objects.filter(user=user, lesson__in=lessons).values_list("lesson_id", "status")
    )


def progress_records(user, lessons):
    """Map of lesson_id -> Progress row for the given user."""
    return {
        row.lesson_id: row
        for row in Progress.objects.filter(user=user, lesson__in=lessons)
    }


class CourseListView(generics.ListAPIView):
    """Published courses with lesson summaries + progress (one round-trip for the UI)."""

    serializer_class = CourseDetailSerializer
    pagination_class = None

    def get_queryset(self):
        return (
            Course.objects.published()
            .with_progress(self.request.user)
            .select_related("skill")
            .prefetch_related("lessons")
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        lessons = [lesson for course in queryset for lesson in course.lessons.all()]
        records = progress_records(request.user, lessons)
        serializer = self.get_serializer(
            queryset,
            many=True,
            context={
                **self.get_serializer_context(),
                "progress_records": records,
                "progress_map": {lid: row.status for lid, row in records.items()},
            },
        )
        return Response(serializer.data)


class CourseDetailView(generics.RetrieveAPIView):
    serializer_class = CourseDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Course.objects.published()
            .with_progress(self.request.user)
            .select_related("skill")
            .prefetch_related("lessons")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        lessons = self.get_object().lessons.all()
        records = progress_records(self.request.user, lessons)
        context["progress_records"] = records
        context["progress_map"] = {lid: row.status for lid, row in records.items()}
        return context


class LessonDetailView(generics.RetrieveAPIView):
    serializer_class = LessonDetailSerializer

    def get_object(self):
        return get_object_or_404(
            Lesson.objects.select_related("course"),
            course__slug=self.kwargs["course_slug"],
            course__is_published=True,
            slug=self.kwargs["lesson_slug"],
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        lesson = self.get_object()
        records = progress_records(self.request.user, [lesson])
        context["progress_records"] = records
        context["progress_map"] = {lid: row.status for lid, row in records.items()}
        return context
