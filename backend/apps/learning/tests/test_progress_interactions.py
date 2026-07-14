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