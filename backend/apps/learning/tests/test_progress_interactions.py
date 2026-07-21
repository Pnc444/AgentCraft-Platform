import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.courses.models import Course, Lesson, Skill
from apps.learning.models import Progress


pytestmark = pytest.mark.django_db


def test_lesson_progress_persists_interaction_events():
    user = get_user_model().objects.create_user(username="student", password="demo1234")
    skill = Skill.objects.create(name="Create an AI Agent", slug="create-an-ai-agent", order=1)
    course = Course.objects.create(
        title="Module 6: OpenClaw (Build #2)",
        slug="module-6-openclaw",
        description="Student-facing OpenClaw module.",
        skill=skill,
        order=8,
        difficulty=2,
        is_published=True,
    )
    lesson = Lesson.objects.create(
        course=course,
        title="Configuration",
        slug="configuration",
        lesson_type=Lesson.LessonType.AGENT_LAB,
        order=1,
        estimated_minutes=15,
        content="Configuration content",
        sandbox_config={"questions": []},
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        f"/api/v1/lessons/{lesson.id}/progress/",
        {
            "status": "in_progress",
            "interaction_event": {
                "type": "artifact_action",
                "key": f"artifact:{lesson.slug}:preview",
                "status": "done",
                "details": {"action": "preview"},
            },
        },
        format="json",
    )

    assert response.status_code == 200
    progress = Progress.objects.get(user=user, lesson=lesson)
    assert progress.interaction_log == response.data["interaction_log"]
    assert progress.interaction_log[0]["key"] == f"artifact:{lesson.slug}:preview"
    assert progress.interaction_log[0]["status"] == "done"


def test_lesson_progress_rejects_unverified_required_video_completion():
    user = get_user_model().objects.create_user(username="video_student", password="demo1234")
    skill = Skill.objects.create(name="Create an AI Agent", slug="create-an-ai-agent", order=1)
    course = Course.objects.create(
        title="Module 1: Introduction to AI",
        slug="module-1-introduction-to-ai",
        description="Student-facing module.",
        skill=skill,
        order=1,
        difficulty=1,
        is_published=True,
    )
    lesson = Lesson.objects.create(
        course=course,
        title="What are LLMs?",
        slug="what-are-llms",
        lesson_type=Lesson.LessonType.THEORY,
        order=1,
        estimated_minutes=8,
        content="Video content",
        video_url="https://www.youtube-nocookie.com/embed/qMxuthTIQq4",
        require_full_watch=True,
        sandbox_config={"questions": []},
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        f"/api/v1/lessons/{lesson.id}/progress/",
        {"video_watched": True},
        format="json",
    )

    assert response.status_code == 400
    assert response.data["missing"] == "video"

    progress = Progress.objects.get(user=user, lesson=lesson)
    assert progress.video_watched is False


def test_lesson_progress_accepts_verified_required_video_completion():
    user = get_user_model().objects.create_user(username="verified_student", password="demo1234")
    skill = Skill.objects.create(name="Create an AI Agent", slug="create-an-ai-agent", order=1)
    course = Course.objects.create(
        title="Module 1: Introduction to AI",
        slug="module-1-introduction-to-ai",
        description="Student-facing module.",
        skill=skill,
        order=1,
        difficulty=1,
        is_published=True,
    )
    lesson = Lesson.objects.create(
        course=course,
        title="What are LLMs?",
        slug="what-are-llms",
        lesson_type=Lesson.LessonType.THEORY,
        order=1,
        estimated_minutes=8,
        content="Video content",
        video_url="https://www.youtube-nocookie.com/embed/qMxuthTIQq4",
        require_full_watch=True,
        sandbox_config={"questions": []},
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        f"/api/v1/lessons/{lesson.id}/progress/",
        {
            "video_watched": True,
            "interaction_event": {
                "type": "video_completion",
                "key": f"video:{lesson.id}:completion",
                "status": "done",
                "details": {
                    "source": "youtube",
                    "duration_seconds": 100,
                    "watched_seconds": 98,
                },
            },
        },
        format="json",
    )

    assert response.status_code == 200
    progress = Progress.objects.get(user=user, lesson=lesson)
    assert progress.video_watched is True
    assert progress.interaction_log[0]["type"] == "video_completion"
