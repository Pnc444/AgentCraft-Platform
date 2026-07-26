from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.courses.beats import derive_beats, explain_streak_problems, validate_beats
from apps.courses.curriculum import (
    CURRICULUM,
    SKILL,
    default_recap_questions,
    load_content,
)
from apps.courses.models import Course, Lesson, Skill
from apps.courses.sandbox_specs import sandbox_spec_for

# MODULE 2 OWNED BY DOUGLAS — exempted from content validation while its
# lessons land. Do not extend this list. (docs/UI-OVERHAUL-PLAN.md §8)
VALIDATION_EXEMPT_SLUGS = {"module-2-exploring-llm-models"}


class Command(BaseCommand):
    help = (
        "Production-safe curriculum sync: upserts courses/lessons by slug from "
        "curriculum.py + content/*.md. Never touches users, badges, or progress on "
        "kept lessons. Preserves admin-set video_url and quiz questions."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--course",
            action="append",
            dest="courses",
            metavar="SLUG",
            help="Only sync this course slug (repeatable). Default: all courses.",
        )
        parser.add_argument(
            "--prune",
            action="store_true",
            help=(
                "Delete lessons that exist in the DB but not in the curriculum spec "
                "for synced courses. WARNING: student progress on those lessons is lost."
            ),
        )
        parser.add_argument(
            "--strict",
            action="store_true",
            help=(
                "Fail (and roll back the whole sync) on content-validation problems: "
                "authored beats breaking the §2 rules, published modules without an "
                "exam, exams recycling recap questions. Default is warn-only so the "
                "container-startup sync keeps booting while content is migrated. "
                "Use --strict in CI."
            ),
        )

    @transaction.atomic
    def handle(self, *args, **options):
        only = set(options["courses"] or [])
        known = {module["slug"] for module in CURRICULUM}
        unknown = only - known
        if unknown:
            raise CommandError(
                f"Unknown course slug(s): {', '.join(sorted(unknown))}. "
                f"Known: {', '.join(sorted(known))}"
            )

        skill, _ = Skill.objects.get_or_create(
            slug=SKILL["slug"],
            defaults={
                "name": SKILL["name"],
                "description": SKILL["description"],
                "order": SKILL["order"],
            },
        )

        created_lessons = 0
        updated_lessons = 0
        problems: list[str] = []

        for module in CURRICULUM:
            if only and module["slug"] not in only:
                continue

            if module["slug"] not in VALIDATION_EXEMPT_SLUGS:
                problems += _module_assessment_problems(module)

            course, course_created = Course.objects.update_or_create(
                slug=module["slug"],
                defaults={
                    "title": module["title"],
                    "description": module["description"],
                    "skill": skill,
                    "order": module["order"],
                    "difficulty": module["difficulty"],
                    # Fail safe: a module must opt in to being published. Matches
                    # Course.is_published's model default. Defaulting to True here
                    # silently published any spec that forgot the key.
                    "is_published": module.get("published", False),
                },
            )
            self.stdout.write(
                f"{'Created' if course_created else 'Synced'} course: {course.title}"
            )

            spec_slugs: list[str] = []
            for index, lesson_spec in enumerate(module["lessons"], start=1):
                title, slug, lesson_type, minutes = lesson_spec[:4]
                spec_config = dict(lesson_spec[4]) if len(lesson_spec) > 4 else {}
                ai_tutor_prompt = spec_config.pop("ai_tutor_prompt", "")
                spec_video_url = (spec_config.pop("video_url", "") or "").strip()
                # Track presence, not just value: an explicit curriculum choice
                # should reach existing lessons, while silence keeps whatever an
                # admin set. Without this, "require_full_watch": False applied to
                # new lessons only and was silently dropped on every re-sync.
                spec_sets_full_watch = "require_full_watch" in spec_config
                spec_require_full_watch = bool(spec_config.pop("require_full_watch", True))
                spec_slugs.append(slug)
                content = load_content(module["slug"], slug, title)

                # Practice-terminal spec, if this lesson has one authored.
                sandbox_spec = sandbox_spec_for(module["slug"], slug)
                if sandbox_spec:
                    spec_config["sandbox"] = sandbox_spec

                if module["slug"] not in VALIDATION_EXEMPT_SLUGS:
                    artifact_paths = tuple(
                        artifact.get("path")
                        for artifact in spec_config.get("artifact_bundle") or []
                        if isinstance(artifact, dict) and artifact.get("path")
                    )
                    label = f"{module['slug']}/{slug}"
                    if spec_config.get("beats"):
                        # Authored beats face the full §2 rule set.
                        problems += validate_beats(
                            spec_config["beats"],
                            artifact_paths=artifact_paths,
                            lesson_label=label,
                        )
                    else:
                        # Derived beats are exempt from the beat-count budget
                        # (splitting a shipped lesson is content work), but NOT
                        # from the passive-streak rule. Exempting them entirely
                        # let the validator report "0 problems" while 39 of 48
                        # lessons ran 2+ explain beats in a row — the model's
                        # central pedagogical rule, silently decorative.
                        problems += explain_streak_problems(
                            derive_beats(
                                content=content,
                                sandbox_config=spec_config,
                                video_url=spec_video_url,
                                title=title,
                                require_full_watch=spec_require_full_watch,
                            ),
                            lesson_label=label,
                        )

                lesson = Lesson.objects.filter(course=course, slug=slug).first()
                if lesson is None:
                    config = spec_config
                    if not config.get("questions"):
                        config["questions"] = default_recap_questions(title, slug)
                    Lesson.objects.create(
                        course=course,
                        title=title,
                        slug=slug,
                        lesson_type=lesson_type,
                        order=index,
                        estimated_minutes=minutes,
                        content=content,
                        video_url=spec_video_url,
                        require_full_watch=spec_require_full_watch,
                        sandbox_config=config,
                        ai_tutor_prompt=ai_tutor_prompt,
                    )
                    created_lessons += 1
                    self.stdout.write(f"  + created lesson: {title}")
                    continue

                lesson.title = title
                lesson.lesson_type = lesson_type
                lesson.order = index
                lesson.estimated_minutes = minutes
                lesson.content = content
                if spec_video_url and not (lesson.video_url or "").strip():
                    lesson.video_url = spec_video_url
                if spec_sets_full_watch:
                    lesson.require_full_watch = spec_require_full_watch
                if spec_config.get("questions"):
                    config = dict(lesson.sandbox_config or {})
                    config.update(spec_config)
                    lesson.sandbox_config = config
                elif not (lesson.sandbox_config or {}).get("questions"):
                    config = dict(lesson.sandbox_config or {})
                    config["questions"] = default_recap_questions(title, slug)
                    lesson.sandbox_config = config
                # Merging never deletes: shed the retired publish_rules key from
                # rows synced before it was removed from the spec.
                if "publish_rules" in (lesson.sandbox_config or {}):
                    config = dict(lesson.sandbox_config)
                    config.pop("publish_rules", None)
                    lesson.sandbox_config = config
                # The sandbox spec is code-owned, not admin-editable, so it syncs
                # regardless of whether this lesson also ships quiz questions.
                if sandbox_spec:
                    config = dict(lesson.sandbox_config or {})
                    config["sandbox"] = sandbox_spec
                    lesson.sandbox_config = config
                if ai_tutor_prompt:
                    lesson.ai_tutor_prompt = ai_tutor_prompt
                lesson.save()
                updated_lessons += 1

            stale = course.lessons.exclude(slug__in=spec_slugs)
            if stale.exists():
                names = ", ".join(stale.values_list("slug", flat=True))
                if options["prune"]:
                    stale.delete()
                    self.stdout.write(
                        self.style.WARNING(f"  - pruned stale lessons: {names}")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  ! stale lessons kept (use --prune to delete): {names}"
                        )
                    )

        if problems:
            self.stdout.write(
                self.style.WARNING(f"\nContent validation: {len(problems)} problem(s)")
            )
            for problem in problems:
                self.stdout.write(self.style.WARNING(f"  ! {problem}"))
            if options["strict"]:
                raise CommandError(
                    "Content validation failed under --strict. The transaction was "
                    "rolled back — nothing was synced."
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Sync complete. Lessons created: {created_lessons}, updated: {updated_lessons}."
            )
        )


def _module_assessment_problems(module: dict) -> list[str]:
    """Plan §6: every published module ends with an exam, and exam items must
    be new — never the recap bank replayed. This is the check that would have
    caught Module 1's recycled exam automatically."""
    problems: list[str] = []
    lesson_specs = module["lessons"]
    quiz_specs = [spec for spec in lesson_specs if spec[2] == "quiz"]

    if module.get("published", False) and not quiz_specs:
        problems.append(f"{module['slug']}: published module has no exam lesson (plan §6)")

    recap_prompts = set()
    for spec in lesson_specs:
        if spec[2] == "quiz" or len(spec) < 5:
            continue
        for question in (spec[4].get("questions") or []):
            prompt = (question.get("prompt") or "").strip().lower()
            if prompt:
                recap_prompts.add(prompt)

    for spec in quiz_specs:
        config = spec[4] if len(spec) > 4 else {}
        recycled = sum(
            1
            for question in (config.get("questions") or [])
            if (question.get("prompt") or "").strip().lower() in recap_prompts
        )
        if recycled:
            problems.append(
                f"{module['slug']}/{spec[1]}: exam recycles {recycled} recap "
                "question(s) — exam items must be new (plan §6)"
            )
    return problems