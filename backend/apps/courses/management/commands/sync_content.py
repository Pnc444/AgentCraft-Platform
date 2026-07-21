from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.courses.curriculum import (
    CURRICULUM,
    SKILL,
    default_recap_questions,
    load_content,
)
from apps.courses.models import Course, Lesson, Skill


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

        for module in CURRICULUM:
            if only and module["slug"] not in only:
                continue

            course, course_created = Course.objects.update_or_create(
                slug=module["slug"],
                defaults={
                    "title": module["title"],
                    "description": module["description"],
                    "skill": skill,
                    "order": module["order"],
                    "difficulty": module["difficulty"],
                    "is_published": module.get("published", True),
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
                spec_require_full_watch = bool(spec_config.pop("require_full_watch", True))
                spec_slugs.append(slug)
                content = load_content(module["slug"], slug, title)

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
                if spec_config.get("questions"):
                    config = dict(lesson.sandbox_config or {})
                    config.update(spec_config)
                    lesson.sandbox_config = config
                elif not (lesson.sandbox_config or {}).get("questions"):
                    config = dict(lesson.sandbox_config or {})
                    config["questions"] = default_recap_questions(title, slug)
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

        self.stdout.write(
            self.style.SUCCESS(
                f"Sync complete. Lessons created: {created_lessons}, updated: {updated_lessons}."
            )
        )