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
        known = {m["slug"] for m in CURRICULUM}
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

        created_l = updated_l = 0
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

            spec_slugs = []
            for i, lesson_spec in enumerate(module["lessons"], start=1):
                title, slug, ltype, minutes = lesson_spec[:4]
                spec_config = dict(lesson_spec[4]) if len(lesson_spec) > 4 else {}
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
                        lesson_type=ltype,
                        order=i,
                        estimated_minutes=minutes,
                        content=content,
                        sandbox_config=config,
                    )
                    created_l += 1
                    self.stdout.write(f"  + created lesson: {title}")
                else:
                    lesson.title = title
                    lesson.lesson_type = ltype
                    lesson.order = i
                    lesson.estimated_minutes = minutes
                    lesson.content = content
                    # Preserve admin-managed fields: video_url, require_full_watch,
                    # ai_tutor_prompt. Quiz questions: spec wins if provided,
                    # otherwise keep whatever is in the DB (admin-edited or default).
                    if spec_config.get("questions"):
                        cfg = dict(lesson.sandbox_config or {})
                        cfg.update(spec_config)
                        lesson.sandbox_config = cfg
                    elif not (lesson.sandbox_config or {}).get("questions"):
                        cfg = dict(lesson.sandbox_config or {})
                        cfg["questions"] = default_recap_questions(title, slug)
                        lesson.sandbox_config = cfg
                    lesson.save()
                    updated_l += 1

            stale = course.lessons.exclude(slug__in=spec_slugs)
            if stale.exists():
                names = ", ".join(stale.values_list("slug", flat=True))
                if options["prune"]:
                    count, _ = stale.delete()
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
                f"Sync complete. Lessons created: {created_l}, updated: {updated_l}."
            )
        )
