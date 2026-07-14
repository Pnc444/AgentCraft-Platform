from copy import deepcopy
from pathlib import Path

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from apps.courses import module_sync_runtime
from apps.courses.module_sync_runtime import load_selected_packs, validate_course_definition
from apps.courses.models import Course, Lesson


pytestmark = pytest.mark.django_db


def test_mission_packs_are_structurally_valid():
    packs = load_selected_packs()
    assert packs
    for pack in packs:
        assert validate_course_definition(pack) == []


def test_mission_packs_reference_artifact_files_without_inline_bodies():
    for pack in load_selected_packs():
        for lesson in pack["lessons"]:
            for artifact in lesson.get("artifacts", []):
                assert "body" not in artifact


def test_module4_validation_requires_guided_blocks_checkpoint_questions_and_artifacts():
    module4_pack = next(pack for pack in load_selected_packs() if pack["slug"] == "module-4-ai-agents")
    broken_pack = deepcopy(module4_pack)
    broken_lesson = broken_pack["lessons"][0]
    broken_lesson["guided_blocks"] = []
    broken_lesson["checkpoint_questions"] = []
    broken_lesson["artifacts"] = []

    errors = validate_course_definition(broken_pack)

    assert "what-an-ai-agent-is must provide at least three guided lesson blocks" in errors
    assert "what-an-ai-agent-is must provide at least three checkpoint questions" in errors
    assert "what-an-ai-agent-is must provide at least one learning artifact" in errors


def test_default_output_root_targets_backend_project_root():
    assert module_sync_runtime.default_output_root() == Path(module_sync_runtime.__file__).resolve().parents[2]


def test_run_module_sync_syncs_modules_and_artifacts(tmp_path: Path):
    call_command(
        "run_module_sync",
        "--mode",
        "run-all",
        "--apply",
        "--output-root",
        str(tmp_path),
    )

    module4 = Course.objects.get(slug="module-4-ai-agents")
    intro = Lesson.objects.get(course=module4, slug="what-an-ai-agent-is")
    assert "agent is a system" in intro.content.lower()
    assert intro.sandbox_config["guided_blocks"]
    assert intro.sandbox_config["checkpoint_questions"]
    assert module4.lessons.count() == 7
    module4_artifact = tmp_path / "lesson_artifacts/agents/agent-map.md"
    assert module4_artifact.exists()
    assert "Goal:" in module4_artifact.read_text(encoding="utf-8")

    openclaw = Course.objects.get(slug="module-6-openclaw")
    configuration = Lesson.objects.get(course=openclaw, slug="configuration")
    assert "openclaw onboard --install-daemon" in configuration.content
    assert configuration.ai_tutor_prompt
    assert configuration.sandbox_config["artifact_bundle"]
    assert configuration.sandbox_config["artifact_bundle"][0]["inspect_prompt"]
    assert configuration.sandbox_config["artifact_bundle"][0]["change_prompt"]
    assert configuration.sandbox_config["artifact_bundle"][0]["body"]
    assert configuration.sandbox_config["guided_blocks"]
    assert configuration.sandbox_config["checkpoint_questions"]
    assert configuration.sandbox_config["questions"][0]["id"] == "openclaw-config-q1"

    openclaw_artifact = tmp_path / "lesson_artifacts/openclaw/config/openclaw.json.template.json5"
    assert openclaw_artifact.exists()
    assert "agent:" in openclaw_artifact.read_text(encoding="utf-8")

    capstone = Course.objects.get(slug="module-8-capstone-safety-evaluation")
    automation = Lesson.objects.get(course=capstone, slug="automation-examples")
    assert automation.sandbox_config["guided_blocks"]
    assert automation.sandbox_config["checkpoint_questions"]
    testing = Lesson.objects.get(course=capstone, slug="testing")
    assert testing.sandbox_config["evaluation_cases"]
    assert testing.sandbox_config["capstone_assignment"]
    assert capstone.is_published is True


def test_run_module_sync_removes_extra_lessons_from_owned_courses(tmp_path: Path):
    call_command(
        "run_module_sync",
        "--mode",
        "run-all",
        "--apply",
        "--output-root",
        str(tmp_path),
    )

    module4 = Course.objects.get(slug="module-4-ai-agents")
    Lesson.objects.create(
        course=module4,
        title="Placeholder Drift",
        slug="placeholder-drift",
        lesson_type=Lesson.LessonType.THEORY,
        order=99,
        estimated_minutes=5,
        content="Old placeholder content",
        sandbox_config={"questions": []},
    )

    call_command(
        "run_module_sync",
        "--mode",
        "run-all",
        "--apply",
        "--output-root",
        str(tmp_path),
    )

    assert not Lesson.objects.filter(course=module4, slug="placeholder-drift").exists()
    assert module4.lessons.count() == 7


def test_validate_mode_fails_when_required_artifact_is_missing(tmp_path: Path):
    call_command(
        "run_module_sync",
        "--mode",
        "run-all",
        "--apply",
        "--output-root",
        str(tmp_path),
    )

    artifact = tmp_path / "lesson_artifacts/openclaw/config/openclaw.json.template.json5"
    artifact.unlink()

    with pytest.raises(CommandError):
        call_command(
            "run_module_sync",
            "--mode",
            "validate",
            "--apply",
            "--output-root",
            str(tmp_path),
        )


def test_validate_mode_fails_when_generated_artifact_drifts_from_source(tmp_path: Path):
    call_command(
        "run_module_sync",
        "--mode",
        "run-all",
        "--apply",
        "--output-root",
        str(tmp_path),
    )

    artifact = tmp_path / "lesson_artifacts/agents/agent-map.md"
    artifact.write_text("# Drifted copy\n", encoding="utf-8")

    with pytest.raises(CommandError):
        call_command(
            "run_module_sync",
            "--mode",
            "validate",
            "--apply",
            "--output-root",
            str(tmp_path),
        )