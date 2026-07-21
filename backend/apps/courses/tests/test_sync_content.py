import pytest
from django.core.management import call_command

from apps.courses.models import Course, Lesson


pytestmark = pytest.mark.django_db


MODULE_1_WHAT_IS_AI_VIDEO_URL = "https://www.youtube-nocookie.com/embed/c0m6yaGlZh4"
MODULE_1_WHAT_ARE_LLMS_VIDEO_URL = "https://www.youtube-nocookie.com/embed/qMxuthTIQq4"
MODULE_1_OTHER_TYPES_OF_AI_VIDEO_URL = "https://www.youtube-nocookie.com/embed/XFZ-rQ8eeR8"
MODULE_1_BRIEF_HISTORY_VIDEO_URL = "https://www.youtube-nocookie.com/embed/FO8Qq025uc8"


@pytest.mark.parametrize(
    ("course_slug", "lesson_slug", "expected_heading"),
    [
        ("module-4-ai-agents", "what-an-ai-agent-is", "# What an Agent Actually Is"),
        ("module-6-openclaw", "configuration", "# Set Up the Home Base"),
        ("module-8-capstone-safety-evaluation", "testing", "# The Release Decision"),
    ],
)
def test_sync_content_uses_markdown_bodies_for_structured_modules(
    course_slug: str, lesson_slug: str, expected_heading: str
):
    call_command("sync_content", courses=[course_slug])

    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(course=course, slug=lesson_slug)

    assert lesson.content.startswith(expected_heading)
    assert lesson.content.strip() != f"{expected_heading}\n\nLesson Content"


def test_sync_content_materializes_structured_module_6_payload():
    call_command("sync_content", courses=["module-6-openclaw"])

    course = Course.objects.get(slug="module-6-openclaw")
    assert list(course.lessons.values_list("slug", flat=True)) == [
        "configuration",
        "adding-skills",
        "channel",
        "agent-safety",
    ]
    lesson = Lesson.objects.get(course=course, slug="configuration")

    assert lesson.content.startswith("# Set Up the Home Base")
    assert lesson.ai_tutor_prompt
    assert lesson.sandbox_config["guided_blocks"]
    assert lesson.sandbox_config["checkpoint_questions"]
    assert lesson.sandbox_config["questions"][0]["id"] == "openclaw-config-q1"

    first_artifact = lesson.sandbox_config["artifact_bundle"][0]
    assert first_artifact["inspect_prompt"]
    assert first_artifact["body"]


@pytest.mark.parametrize(
    ("course_slug", "lesson_slug", "expected_heading"),
    [
        ("module-5-hermes", "docker-as-backend", "# Docker as Backend"),
        ("module-1-introduction-to-ai", "what-is-ai", "# What is AI?"),
        ("module-1-introduction-to-ai", "what-are-llms", "# What are LLMs?"),
        ("module-1-introduction-to-ai", "what-is-an-llm-model", "# Other Types of AI"),
        ("module-1-introduction-to-ai", "checkpoint", "# Module 1 Exam"),
        ("module-1-introduction-to-ai", "brief-history", "# Brief History"),
    ],
)
def test_sync_content_prefers_markdown_files_over_placeholder_content(
    course_slug: str, lesson_slug: str, expected_heading: str
):
    call_command("sync_content", courses=[course_slug])

    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(course=course, slug=lesson_slug)

    assert lesson.content.startswith(expected_heading)
    assert "Filler lesson" not in lesson.content


def test_sync_content_backfills_curriculum_video_url_without_overwriting_custom_value():
    call_command("sync_content", courses=["module-1-introduction-to-ai"])

    course = Course.objects.get(slug="module-1-introduction-to-ai")
    lesson = Lesson.objects.get(course=course, slug="what-is-ai")

    assert lesson.video_url == MODULE_1_WHAT_IS_AI_VIDEO_URL

    lesson.video_url = ""
    lesson.save(update_fields=["video_url"])

    call_command("sync_content", courses=["module-1-introduction-to-ai"])
    lesson.refresh_from_db()

    assert lesson.video_url == MODULE_1_WHAT_IS_AI_VIDEO_URL

    custom_url = "https://youtu.be/dQw4w9WgXcQ"
    lesson.video_url = custom_url
    lesson.save(update_fields=["video_url"])

    call_command("sync_content", courses=["module-1-introduction-to-ai"])
    lesson.refresh_from_db()

    assert lesson.video_url == custom_url


def test_sync_content_uses_curriculum_recap_questions_for_module_1_video_lesson():
    call_command("sync_content", courses=["module-1-introduction-to-ai"])

    course = Course.objects.get(slug="module-1-introduction-to-ai")
    lesson = Lesson.objects.get(course=course, slug="what-is-ai")

    questions = lesson.sandbox_config["questions"]

    assert len(questions) == 5
    assert questions[0]["id"] == "m1-ai-video-q1"
    assert questions[0]["answer_index"] == 0
    assert "human intelligence" in questions[0]["options"][0]
    assert all(question["id"].startswith("m1-ai-video-") for question in questions)


def test_sync_content_uses_curriculum_recap_questions_for_module_1_llm_video_lesson():
    call_command("sync_content", courses=["module-1-introduction-to-ai"])

    course = Course.objects.get(slug="module-1-introduction-to-ai")
    lesson = Lesson.objects.get(course=course, slug="what-are-llms")

    questions = lesson.sandbox_config["questions"]

    assert lesson.video_url == MODULE_1_WHAT_ARE_LLMS_VIDEO_URL
    assert len(questions) == 5
    assert questions[0]["id"] == "m1-llm-video-q1"
    assert questions[0]["answer_index"] == 0
    assert "humanlike text" in questions[0]["options"][0]
    assert all(question["id"].startswith("m1-llm-video-") for question in questions)


def test_sync_content_uses_curriculum_recap_questions_for_module_1_other_ai_video_lesson():
    call_command("sync_content", courses=["module-1-introduction-to-ai"])

    course = Course.objects.get(slug="module-1-introduction-to-ai")
    lesson = Lesson.objects.get(course=course, slug="what-is-an-llm-model")

    questions = lesson.sandbox_config["questions"]

    assert lesson.video_url == MODULE_1_OTHER_TYPES_OF_AI_VIDEO_URL
    assert len(questions) == 5
    assert questions[0]["id"] == "m1-other-ai-q1"
    assert questions[0]["answer_index"] == 0
    assert "capabilities" in questions[0]["options"][0]
    assert all(question["id"].startswith("m1-other-ai-") for question in questions)


def test_sync_content_uses_curriculum_recap_questions_for_module_1_brief_history_video_lesson():
    call_command("sync_content", courses=["module-1-introduction-to-ai"])

    course = Course.objects.get(slug="module-1-introduction-to-ai")
    lesson = Lesson.objects.get(course=course, slug="brief-history")

    questions = lesson.sandbox_config["questions"]

    assert lesson.video_url == MODULE_1_BRIEF_HISTORY_VIDEO_URL
    assert len(questions) == 5
    assert questions[0]["id"] == "m1-history-q1"
    assert questions[0]["answer_index"] == 0
    assert "Can machines think?" in questions[0]["options"][0]
    assert all(question["id"].startswith("m1-history-") for question in questions)


def test_sync_content_uses_full_module_1_exam_question_bank():
    call_command("sync_content", courses=["module-1-introduction-to-ai"])

    course = Course.objects.get(slug="module-1-introduction-to-ai")
    lesson = Lesson.objects.get(course=course, slug="checkpoint")

    questions = lesson.sandbox_config["questions"]

    assert lesson.title == "Module 1 Exam"
    assert len(questions) == 20
    assert questions[0]["id"] == "m1-ai-video-q1"
    assert questions[5]["id"] == "m1-llm-video-q1"
    assert questions[10]["id"] == "m1-other-ai-q1"
    assert questions[15]["id"] == "m1-history-q1"
