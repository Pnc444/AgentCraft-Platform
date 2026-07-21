from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.courses.models import Lesson

from .badges import badges_for_user, evaluate_badges_for_user
from .models import Progress, Recommendation
from .serializers import ProgressSerializer, ProgressUpdateSerializer, RecommendationSerializer


VIDEO_COMPLETION_BUFFER_SECONDS = 3.0
VIDEO_COMPLETION_MIN_RATIO = 0.95


def upsert_interaction_event(log: list[dict], event: dict) -> list[dict]:
    next_log = [entry for entry in log if isinstance(entry, dict)]
    normalized = {
        "type": event["type"].strip(),
        "key": event["key"].strip(),
        "status": event.get("status", "done"),
        "timestamp": timezone.now().isoformat(),
        "details": event.get("details", {}),
    }

    for index, existing in enumerate(next_log):
        if existing.get("key") != normalized["key"]:
            continue
        next_log[index] = normalized
        break
    else:
        next_log.append(normalized)

    return next_log


def _coerce_non_negative_float(value) -> float | None:
    if isinstance(value, (int, float)):
        parsed = float(value)
    elif isinstance(value, str):
        try:
            parsed = float(value)
        except ValueError:
            return None
    else:
        return None

    if parsed < 0:
        return None
    return parsed


def _video_completion_verified(event: dict | None) -> bool:
    if not isinstance(event, dict):
        return False
    if event.get("type") != "video_completion":
        return False

    details = event.get("details")
    if not isinstance(details, dict):
        return False

    duration_seconds = _coerce_non_negative_float(details.get("duration_seconds"))
    watched_seconds = _coerce_non_negative_float(details.get("watched_seconds"))

    if not duration_seconds or watched_seconds is None:
        return False

    threshold = max(
        duration_seconds - VIDEO_COMPLETION_BUFFER_SECONDS,
        duration_seconds * VIDEO_COMPLETION_MIN_RATIO,
    )
    return watched_seconds >= threshold


class LessonProgressView(APIView):
    """POST /lessons/{id}/progress/ — create or update the user's progress on a lesson."""

    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id, course__is_published=True)
        serializer = ProgressUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        progress, _ = Progress.objects.get_or_create(user=request.user, lesson=lesson)
        interaction_event = serializer.validated_data.pop("interaction_event", None)
        requested_video_watched = serializer.validated_data.pop("video_watched", None)
        for field, value in serializer.validated_data.items():
            setattr(progress, field, value)
        if interaction_event:
            progress.interaction_log = upsert_interaction_event(progress.interaction_log, interaction_event)
        completion_verified = _video_completion_verified(interaction_event)
        if completion_verified:
            progress.video_watched = True
        elif requested_video_watched is True and (lesson.video_url or "").strip() and lesson.require_full_watch:
            return Response(
                {
                    "detail": "Video completion could not be verified. Finish the lesson video in the built-in player before continuing.",
                    "missing": "video",
                },
                status=400,
            )
        elif requested_video_watched is not None:
            progress.video_watched = requested_video_watched
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
