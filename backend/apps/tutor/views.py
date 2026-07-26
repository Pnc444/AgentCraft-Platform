"""Streaming tutor endpoint.

Streams because a 550B model takes several seconds to finish a paragraph, and a
stuck beginner staring at a spinner is a beginner who closes the tab. First
token lands in about a second; the rest arrives as it is written.

Transport is SSE over a plain POST rather than EventSource, because EventSource
cannot set an Authorization header and the tutor must be authenticated.
"""

from __future__ import annotations

import json
import logging

from django.conf import settings
from django.core.cache import cache
from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.courses.models import Lesson

from .client import TutorUnavailable, stream_chat
from .context import build_system_prompt, suggested_questions

logger = logging.getLogger(__name__)

MAX_MESSAGE_CHARS = 2000
MAX_HISTORY_TURNS = 8

RATE_LIMIT_REQUESTS = 20
RATE_LIMIT_WINDOW_SECONDS = 300


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


def _rate_limited(user_id: int) -> bool:
    """Crude fixed-window limiter. Protects the shared free-tier key."""
    key = f"tutor:rl:{user_id}"
    hits = cache.get(key, 0)
    if hits >= RATE_LIMIT_REQUESTS:
        return True
    # add() sets only if missing, so the window starts on the first hit.
    if cache.add(key, 1, RATE_LIMIT_WINDOW_SECONDS) is False:
        try:
            cache.incr(key)
        except ValueError:
            cache.set(key, 1, RATE_LIMIT_WINDOW_SECONDS)
    return False


class TutorAskView(APIView):
    """POST a question, get back an SSE stream of the answer."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # EnvelopeRenderer wraps these into { data, meta, errors } automatically.
        message = (request.data.get("message") or "").strip()
        if not message:
            return Response(
                ["Ask a question first."], status=status.HTTP_400_BAD_REQUEST
            )
        if len(message) > MAX_MESSAGE_CHARS:
            return Response(
                [f"Keep it under {MAX_MESSAGE_CHARS} characters."],
                status=status.HTTP_400_BAD_REQUEST,
            )
        if _rate_limited(request.user.id):
            return Response(
                [
                    "You've asked a lot of questions very quickly. "
                    "Give it a few minutes."
                ],
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        lesson = self._resolve_lesson(request.data)
        messages = [{"role": "system", "content": build_system_prompt(request.user, lesson)}]
        messages.extend(self._clean_history(request.data.get("history")))
        messages.append({"role": "user", "content": message})

        response = StreamingHttpResponse(
            self._stream(messages),
            content_type="text/event-stream",
        )
        # Defeat proxy buffering, which would otherwise defeat the point.
        response["Cache-Control"] = "no-cache, no-transform"
        response["X-Accel-Buffering"] = "no"
        return response

    def _resolve_lesson(self, data) -> Lesson | None:
        course_slug = (data.get("course_slug") or "").strip()
        lesson_slug = (data.get("lesson_slug") or "").strip()
        if not (course_slug and lesson_slug):
            return None
        return (
            Lesson.objects.select_related("course")
            .filter(
                course__slug=course_slug,
                slug=lesson_slug,
                course__is_published=True,
            )
            .first()
        )

    def _clean_history(self, history) -> list[dict]:
        """Trust nothing from the client except role and text."""
        if not isinstance(history, list):
            return []
        cleaned: list[dict] = []
        for item in history[-(MAX_HISTORY_TURNS * 2) :]:
            if not isinstance(item, dict):
                continue
            role = item.get("role")
            text = (item.get("text") or item.get("content") or "").strip()
            if role in ("user", "assistant") and text:
                cleaned.append({"role": role, "content": text[:MAX_MESSAGE_CHARS]})
        return cleaned

    def _stream(self, messages):
        try:
            for event, value in stream_chat(messages):
                if event == "model":
                    yield _sse("model", {"model": value})
                else:
                    yield _sse("token", {"text": value})
            yield _sse("done", {})
        except TutorUnavailable as exc:
            logger.warning("tutor unavailable: %s", exc.detail)
            yield _sse("error", {"message": exc.learner_message})
        except Exception:  # noqa: BLE001 - never leak a traceback into the stream
            logger.exception("tutor stream crashed")
            yield _sse("error", {"message": "The tutor hit an unexpected error."})


class TutorSuggestionsView(APIView):
    """Starter prompts for the empty state."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        course_slug = (request.query_params.get("course_slug") or "").strip()
        lesson_slug = (request.query_params.get("lesson_slug") or "").strip()
        lesson = None
        if course_slug and lesson_slug:
            lesson = (
                Lesson.objects.select_related("course")
                .filter(
                    course__slug=course_slug,
                    slug=lesson_slug,
                    course__is_published=True,
                )
                .first()
            )
        return Response(
            {
                "suggestions": suggested_questions(lesson),
                "available": bool(settings.OPENROUTER_API_KEY),
            }
        )
