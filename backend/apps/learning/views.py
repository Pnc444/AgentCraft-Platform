from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.courses.models import Lesson

from .badges import badges_for_user, evaluate_badges_for_user
from .models import Progress, Recommendation
from .serializers import ProgressSerializer, ProgressUpdateSerializer, RecommendationSerializer


class LessonProgressView(APIView):
    """POST /lessons/{id}/progress/ — create or update the user's progress on a lesson."""

    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id, course__is_published=True)
        serializer = ProgressUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        progress, _ = Progress.objects.get_or_create(user=request.user, lesson=lesson)
        for field, value in serializer.validated_data.items():
            setattr(progress, field, value)
        progress.last_attempt_at = timezone.now()
        # Completing a lesson may require finishing the video first (admin toggle).
        if (
            progress.status == Progress.Status.COMPLETED
            and (lesson.video_url or "").strip()
            and lesson.require_full_watch
            and not progress.video_watched
        ):
            return Response(
                {
                    "detail": "Watch the lesson video before completing this lesson.",
                    "missing": "video",
                },
                status=400,
            )
        if progress.status == Progress.Status.COMPLETED:
            score = progress.score
            if score is None or score < 80:
                return Response(
                    {
                        "detail": "Pass the Recap Quiz with 80% or higher to complete this lesson.",
                        "missing": "quiz",
                    },
                    status=400,
                )
            if progress.completed_at is None:
                progress.completed_at = timezone.now()
        elif "status" in serializer.validated_data:
            progress.completed_at = None
        progress.save()

        if progress.status == Progress.Status.COMPLETED:
            evaluate_badges_for_user(request.user)

        return Response(ProgressSerializer(progress).data)


class RecommendationListView(generics.ListAPIView):
    serializer_class = RecommendationSerializer
    pagination_class = None

    def get_queryset(self):
        return (
            Recommendation.objects.filter(user=self.request.user, is_read=False)
            .select_related("lesson__course")
            .order_by("-confidence")[:5]
        )


class DashboardStatsView(APIView):
    """GET /dashboard/stats/ — profile stats + badges for the current user."""

    def get(self, request):
        user = request.user
        lessons_completed = Progress.objects.filter(
            user=user, status=Progress.Status.COMPLETED
        ).count()
        lessons_in_progress = Progress.objects.filter(
            user=user, status=Progress.Status.IN_PROGRESS
        ).count()
        total_lessons = Lesson.objects.filter(course__is_published=True).count()
        overall_progress_pct = (
            round(lessons_completed / total_lessons * 100) if total_lessons else 0
        )
        badges = badges_for_user(user)
        return Response(
            {
                "lessons_completed": lessons_completed,
                "lessons_in_progress": lessons_in_progress,
                "total_lessons": total_lessons,
                "overall_progress_pct": overall_progress_pct,
                "badges": badges,
                "badges_unlocked": sum(1 for b in badges if b["unlocked"]),
                "badges_total": len(badges),
            }
        )
