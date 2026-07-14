from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from apps.courses.module_missions import get_mission_packs
from apps.courses.models import Course, Lesson, Skill

PLACEHOLDER_TEMPLATE = "# {title}\n\nLesson Content"
COURSE_SKILL_SLUG = "create-an-ai-agent"
MODULE_4_SLUG = "module-4-ai-agents"
MODULE_6_SLUG = "module-6-openclaw"
MODULE_8_SLUG = "module-8-capstone-safety-evaluation"
STRUCTURED_KEYS = (
    "artifact_bundle",
    "skill_templates",
    "channel_templates",
    "safety_checks",
    "permission_matrix",
    "evaluation_rubric",
    "evaluation_cases",
    "guided_blocks",
    "checkpoint_questions",
    "capstone_assignment",
    "publish_rules",
)
AUTHORED_LESSON_KEYS = (
    "skill_templates",
    "channel_templates",
    "safety_checks",
    "permission_matrix",
    "evaluation_rubric",
    "evaluation_cases",
)


def default_output_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_sandbox_config(lesson_pack: dict) -> dict:
    sandbox_config = {key: deepcopy(lesson_pack.get(key, [])) for key in STRUCTURED_KEYS}
    sandbox_config["questions"] = deepcopy(lesson_pack.get("questions", []))
    sandbox_config["artifact_bundle"] = deepcopy(lesson_pack.get("artifacts", []))
    return sandbox_config


def is_placeholder_content(title: str, content: str) -> bool:
    return content.strip() == PLACEHOLDER_TEMPLATE.format(title=title).strip()


def _validate_question(question: dict, lesson_slug: str, index: int) -> list[str]:
    errors: list[str] = []
    question_id = question.get("id")
    prompt = question.get("prompt")
    options = question.get("options")
    answer_index = question.get("answer_index")
    prefix = f"{lesson_slug} question {index + 1}"

    if not isinstance(question_id, str) or not question_id.strip():
        errors.append(f"{prefix} is missing a non-empty id")
    if not isinstance(prompt, str) or not prompt.strip():
        errors.append(f"{prefix} is missing a prompt")
    if not isinstance(options, list) or len(options) < 3:
        errors.append(f"{prefix} must define at least three options")
    elif any(not isinstance(option, str) or not option.strip() for option in options):
        errors.append(f"{prefix} contains a blank option")
    if not isinstance(answer_index, int):
        errors.append(f"{prefix} is missing an integer answer_index")
    elif isinstance(options, list) and (answer_index < 0 or answer_index >= len(options)):
        errors.append(f"{prefix} answer_index is out of range")
    return errors


def _validate_artifact(artifact: dict, lesson_slug: str, index: int) -> list[str]:
    errors: list[str] = []
    path = artifact.get("path")
    summary = artifact.get("summary")
    artifact_format = artifact.get("format")
    body = artifact.get("body")
    prefix = f"{lesson_slug} artifact {index + 1}"

    if not isinstance(path, str) or not path.strip():
        errors.append(f"{prefix} is missing a path")
    elif Path(path).is_absolute() or ".." in Path(path).parts:
        errors.append(f"{prefix} path must stay inside the repo")
    if not isinstance(summary, str) or not summary.strip():
        errors.append(f"{prefix} is missing a summary")
    if artifact_format not in {"text", "json"}:
        errors.append(f"{prefix} format must be 'text' or 'json'")
    if artifact_format == "text" and not isinstance(body, str):
        errors.append(f"{prefix} text artifacts must use a string body")
    if artifact_format == "json" and not isinstance(body, (dict, list)):
        errors.append(f"{prefix} json artifacts must use an object or array body")
    return errors


def _validate_guided_block(block: dict, lesson_slug: str, index: int) -> list[str]:
    errors: list[str] = []
    prefix = f"{lesson_slug} guided block {index + 1}"
    if not isinstance(block, dict):
        return [f"{prefix} must be an object"]
    if not isinstance(block.get("title"), str) or not block["title"].strip():
        errors.append(f"{prefix} is missing a title")
    if not isinstance(block.get("body"), str) or not block["body"].strip():
        errors.append(f"{prefix} is missing a body")
    for field in ("analogy", "remember"):
        value = block.get(field)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            errors.append(f"{prefix} field {field} must be a non-empty string when provided")
    try_this = block.get("try_this")
    if try_this is not None:
        if not isinstance(try_this, list) or any(
            not isinstance(item, str) or not item.strip() for item in try_this
        ):
            errors.append(f"{prefix} try_this must be a list of non-empty strings")
    checkpoint_after = block.get("checkpoint_after")
    if checkpoint_after is not None and not isinstance(checkpoint_after, bool):
        errors.append(f"{prefix} checkpoint_after must be a boolean when provided")
    block_questions = block.get("checkpoint_questions")
    if block_questions is not None:
        if not isinstance(block_questions, list):
            errors.append(f"{prefix} checkpoint_questions must be a list when provided")
        else:
            for question_index, question in enumerate(block_questions):
                errors.extend(
                    _validate_question(question, f"{lesson_slug} guided block {index + 1}", question_index)
                )
    kind = block.get("kind")
    if kind is not None and kind not in {"common_mistake", "teach_it_back"}:
        errors.append(f"{prefix} kind must be 'common_mistake' or 'teach_it_back' when provided")
    return errors


def validate_course_definition(course_pack: dict) -> list[str]:
    errors: list[str] = []
    required_course_keys = {"title", "slug", "description", "difficulty", "order", "lessons"}
    missing = sorted(required_course_keys - course_pack.keys())
    if missing:
        errors.append(f"{course_pack.get('slug', 'unknown-course')} is missing keys: {', '.join(missing)}")
        return errors

    lessons = course_pack.get("lessons", [])
    if not isinstance(lessons, list) or not lessons:
        errors.append(f"{course_pack['slug']} must define at least one lesson")
        return errors

    for lesson in lessons:
        lesson_slug = lesson.get("slug", "unknown-lesson")
        lesson_title = lesson.get("title", "Untitled")
        for key in ("title", "slug", "lesson_type", "estimated_minutes", "content", "ai_tutor_prompt"):
            if key not in lesson or not lesson[key]:
                errors.append(f"{lesson_slug} is missing {key}")
        if isinstance(lesson.get("content"), str) and is_placeholder_content(lesson_title, lesson["content"]):
            errors.append(f"{lesson_slug} still uses placeholder content")

        questions = lesson.get("questions", [])
        if len(questions) < 5:
            errors.append(f"{lesson_slug} must define at least five recap questions")
        for index, question in enumerate(questions):
            errors.extend(_validate_question(question, lesson_slug, index))

        for structured_key in AUTHORED_LESSON_KEYS:
            if structured_key not in lesson:
                errors.append(f"{lesson_slug} is missing structured key {structured_key}")

        for index, block in enumerate(lesson.get("guided_blocks", [])):
            errors.extend(_validate_guided_block(block, lesson_slug, index))

        for index, question in enumerate(lesson.get("checkpoint_questions", [])):
            errors.extend(_validate_question(question, f"{lesson_slug} checkpoint", index))

        for index, artifact in enumerate(lesson.get("artifacts", [])):
            errors.extend(_validate_artifact(artifact, lesson_slug, index))

    if course_pack["slug"] == MODULE_6_SLUG:
        if not any(lesson.get("skill_templates") for lesson in lessons):
            errors.append(f"{MODULE_6_SLUG} must provide at least one skill template")
        if not any(lesson.get("channel_templates") for lesson in lessons):
            errors.append(f"{MODULE_6_SLUG} must provide at least one channel template")
        if not any(lesson.get("safety_checks") for lesson in lessons):
            errors.append(f"{MODULE_6_SLUG} must provide at least one safety check")
        for lesson in lessons:
            lesson_slug = lesson.get("slug", "unknown-lesson")
            if len(lesson.get("guided_blocks", [])) < 3:
                errors.append(f"{lesson_slug} must provide at least three guided lesson blocks")
            if len(lesson.get("checkpoint_questions", [])) < 3:
                errors.append(f"{lesson_slug} must provide at least three checkpoint questions")

        if course_pack["slug"] == MODULE_4_SLUG:
            for lesson in lessons:
                lesson_slug = lesson.get("slug", "unknown-lesson")
                if len(lesson.get("guided_blocks", [])) < 3:
                    errors.append(f"{lesson_slug} must provide at least three guided lesson blocks")
                if len(lesson.get("checkpoint_questions", [])) < 3:
                    errors.append(f"{lesson_slug} must provide at least three checkpoint questions")
                if not lesson.get("artifacts"):
                    errors.append(f"{lesson_slug} must provide at least one learning artifact")

    if course_pack["slug"] == MODULE_8_SLUG:
        if not any(lesson.get("permission_matrix") for lesson in lessons):
            errors.append(f"{MODULE_8_SLUG} must provide at least one permission matrix")
        if not any(lesson.get("evaluation_rubric") for lesson in lessons):
            errors.append(f"{MODULE_8_SLUG} must provide at least one evaluation rubric")
        if not any(lesson.get("evaluation_cases") for lesson in lessons):
            errors.append(f"{MODULE_8_SLUG} must provide at least one evaluation case set")
        for lesson in lessons:
            lesson_slug = lesson.get("slug", "unknown-lesson")
            if len(lesson.get("guided_blocks", [])) < 3:
                errors.append(f"{lesson_slug} must provide at least three guided lesson blocks")
            if len(lesson.get("checkpoint_questions", [])) < 3:
                errors.append(f"{lesson_slug} must provide at least three checkpoint questions")
            if lesson_slug == "testing" and not isinstance(lesson.get("capstone_assignment"), dict):
                errors.append("testing must provide a capstone_assignment")

    return errors


def ensure_skill(apply: bool) -> Skill | None:
    defaults = {
        "name": "Create an AI Agent",
        "description": "Build AI agents from foundations through capstone",
        "order": 1,
    }
    if not apply:
        return Skill.objects.filter(slug=COURSE_SKILL_SLUG).first()
    skill, _ = Skill.objects.get_or_create(slug=COURSE_SKILL_SLUG, defaults=defaults)
    return skill


def write_artifacts(lesson_pack: dict, output_root: Path, apply: bool) -> list[dict]:
    writes: list[dict] = []
    for artifact in lesson_pack.get("artifacts", []):
        target_path = output_root / artifact["path"]
        writes.append({"path": str(target_path), "summary": artifact["summary"], "applied": apply})
        if not apply:
            continue
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if artifact["format"] == "json":
            target_path.write_text(json.dumps(artifact["body"], indent=2) + "\n", encoding="utf-8")
        else:
            target_path.write_text(artifact["body"], encoding="utf-8")
    return writes


def cleanup_extra_artifacts(course_pack: dict, output_root: Path, apply: bool) -> list[str]:
    expected_paths = {
        (output_root / artifact["path"]).resolve()
        for lesson in course_pack["lessons"]
        for artifact in lesson.get("artifacts", [])
    }
    roots = {
        output_root / Path(artifact["path"]).parts[0] / Path(artifact["path"]).parts[1]
        for lesson in course_pack["lessons"]
        for artifact in lesson.get("artifacts", [])
    }
    removed: list[str] = []

    if not apply:
        return removed

    for root in roots:
        if not root.exists():
            continue
        for file_path in sorted(path for path in root.rglob("*") if path.is_file()):
            resolved = file_path.resolve()
            if resolved in expected_paths:
                continue
            file_path.unlink()
            removed.append(str(file_path))

        for dir_path in sorted((path for path in root.rglob("*") if path.is_dir()), reverse=True):
            if any(dir_path.iterdir()):
                continue
            dir_path.rmdir()

    return removed


def sync_course_pack(course_pack: dict, output_root: Path, apply: bool) -> dict:
    lesson_reports: list[dict] = []
    warnings: list[str] = []
    removed_lessons: list[str] = []
    removed_artifacts = cleanup_extra_artifacts(course_pack, output_root, apply)
    skill = ensure_skill(apply)
    existing_course = Course.objects.filter(slug=course_pack["slug"]).first()
    created = existing_course is None

    if apply:
        if skill is None:
            raise RuntimeError("Create an AI Agent skill is required before syncing mission packs")
        course, _ = Course.objects.get_or_create(
            slug=course_pack["slug"],
            defaults={
                "title": course_pack["title"],
                "description": course_pack["description"],
                "skill": skill,
                "order": course_pack["order"],
                "difficulty": course_pack["difficulty"],
                "is_published": False,
            },
        )
        course.title = course_pack["title"]
        course.description = course_pack["description"]
        course.skill = skill
        course.order = course_pack["order"]
        course.difficulty = course_pack["difficulty"]
        course.save()
    else:
        course = existing_course

    existing_lesson_slugs = set()
    if course is not None:
        existing_lesson_slugs = set(course.lessons.values_list("slug", flat=True))

    pack_lesson_slugs = {lesson["slug"] for lesson in course_pack["lessons"]}
    extra_slugs = sorted(existing_lesson_slugs - pack_lesson_slugs)
    if extra_slugs:
        if apply and course is not None:
            Lesson.objects.filter(course=course, slug__in=extra_slugs).delete()
            removed_lessons = extra_slugs
        else:
            warnings.append(
                f"{course_pack['slug']} has extra lessons not owned by Headmaster: {', '.join(extra_slugs)}"
            )

    for order, lesson_pack in enumerate(course_pack["lessons"], start=1):
        sandbox_config = build_sandbox_config(lesson_pack)
        artifact_writes = write_artifacts(lesson_pack, output_root, apply)
        lesson_report = {
            "slug": lesson_pack["slug"],
            "title": lesson_pack["title"],
            "created": False,
            "updated": False,
            "artifact_writes": artifact_writes,
        }

        if apply and course is not None:
            lesson, was_created = Lesson.objects.get_or_create(
                course=course,
                slug=lesson_pack["slug"],
                defaults={
                    "title": lesson_pack["title"],
                    "lesson_type": lesson_pack["lesson_type"],
                    "order": order,
                    "estimated_minutes": lesson_pack["estimated_minutes"],
                    "content": lesson_pack["content"],
                    "video_url": lesson_pack.get("video_url", ""),
                    "sandbox_config": sandbox_config,
                    "ai_tutor_prompt": lesson_pack["ai_tutor_prompt"],
                },
            )
            lesson.title = lesson_pack["title"]
            lesson.lesson_type = lesson_pack["lesson_type"]
            lesson.order = order
            lesson.estimated_minutes = lesson_pack["estimated_minutes"]
            lesson.content = lesson_pack["content"]
            lesson.video_url = lesson_pack.get("video_url", "")
            lesson.sandbox_config = sandbox_config
            lesson.ai_tutor_prompt = lesson_pack["ai_tutor_prompt"]
            lesson.save()
            lesson_report["created"] = was_created
            lesson_report["updated"] = True

        lesson_reports.append(lesson_report)

    return {
        "slug": course_pack["slug"],
        "title": course_pack["title"],
        "created": created,
        "synced": apply,
        "warnings": warnings,
        "removed_lessons": removed_lessons,
        "removed_artifacts": removed_artifacts,
        "lessons": lesson_reports,
    }


def validate_synced_course(course_pack: dict, output_root: Path) -> list[str]:
    errors = validate_course_definition(course_pack)
    if errors:
        return errors

    course = Course.objects.filter(slug=course_pack["slug"]).first()
    if course is None:
        return [f"{course_pack['slug']} does not exist in the database"]

    for order, lesson_pack in enumerate(course_pack["lessons"], start=1):
        lesson = Lesson.objects.filter(course=course, slug=lesson_pack["slug"]).first()
        if lesson is None:
            errors.append(f"{course_pack['slug']} is missing lesson {lesson_pack['slug']}")
            continue
        if lesson.title != lesson_pack["title"]:
            errors.append(f"{lesson_pack['slug']} title drifted from the mission pack")
        if lesson.lesson_type != lesson_pack["lesson_type"]:
            errors.append(f"{lesson_pack['slug']} lesson_type drifted from the mission pack")
        if lesson.order != order:
            errors.append(f"{lesson_pack['slug']} order drifted from the mission pack")
        if is_placeholder_content(lesson_pack["title"], lesson.content):
            errors.append(f"{lesson_pack['slug']} still has placeholder content in the database")
        if lesson.content != lesson_pack["content"]:
            errors.append(f"{lesson_pack['slug']} content does not match the mission pack")
        if lesson.ai_tutor_prompt != lesson_pack["ai_tutor_prompt"]:
            errors.append(f"{lesson_pack['slug']} ai_tutor_prompt does not match the mission pack")
        expected_config = build_sandbox_config(lesson_pack)
        if lesson.sandbox_config != expected_config:
            errors.append(f"{lesson_pack['slug']} sandbox_config does not match the mission pack")
        for artifact in lesson_pack.get("artifacts", []):
            artifact_path = output_root / artifact["path"]
            if not artifact_path.exists():
                errors.append(f"{lesson_pack['slug']} is missing artifact {artifact['path']}")

    return errors


def publish_course_pack(course_pack: dict, apply: bool) -> dict:
    course = Course.objects.get(slug=course_pack["slug"])
    if apply:
        course.is_published = True
        course.save(update_fields=["is_published"])
    return {
        "slug": course.slug,
        "published": apply or course.is_published,
        "applied": apply,
    }


def load_selected_packs(selected_slugs: list[str] | None = None) -> list[dict]:
    packs = get_mission_packs()
    if not selected_slugs:
        return packs
    selected = set(selected_slugs)
    return [pack for pack in packs if pack["slug"] in selected]