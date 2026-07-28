from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.accounts.models import User
from apps.courses.models import Course, Lesson
from apps.learning.badges import evaluate_badges_for_user
from apps.learning.models import Progress


class Command(BaseCommand):
    help = "Mark all lessons complete for the demo user. Defaults to modules 1 and 1.5."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            default="demo_student",
            help="Username to update (default: demo_student)",
        )
        parser.add_argument(
            "--course-slug",
            action="append",
            dest="course_slugs",
            help=(
                "Course slug to include. Repeat for multiple courses. "
                "Defaults to modules 1 and 1.5."
            ),
        )

    def handle(self, *args, **options):
        username = options["username"]
        course_slugs = options["course_slugs"] or [
            "module-1-introduction-to-ai",
            "module-1-5-how-llms-work",
        ]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as exc:
            raise CommandError(f"User {username!r} does not exist.") from exc

        courses = list(
            Course.objects.filter(is_published=True, slug__in=course_slugs).order_by(
                "order", "skill__order", "title"
            )
        )
        found_slugs = {course.slug for course in courses}
        missing_slugs = [slug for slug in course_slugs if slug not in found_slugs]
        if missing_slugs:
            raise CommandError(
                f"No matching published course found for: {', '.join(missing_slugs)}."
            )

        completed_count = 0
        now = timezone.now()

        for course in courses:
            lessons = Lesson.objects.filter(course=course).order_by("order")
            for lesson in lessons:
                Progress.objects.update_or_create(
                    user=user,
                    lesson=lesson,
                    defaults={
                        "status": Progress.Status.COMPLETED,
                        "completed_at": now,
                    },
                )
                completed_count += 1

        evaluate_badges_for_user(user)

        self.stdout.write(
            self.style.SUCCESS(
                f"Marked {completed_count} lesson(s) complete for {user.username} in {', '.join(course_slugs)}."
            )
        )