from django.core.management.base import BaseCommand

from apps.accounts.models import User
from apps.courses.curriculum import CURRICULUM, SKILL, default_recap_questions, load_content
from apps.courses.models import Course, Lesson, Skill
from apps.learning.badges import evaluate_badges_for_user, seed_badges
from apps.learning.models import Progress, UserBadge


class Command(BaseCommand):
    help = (
        "DEV ONLY: full reset — wipes all courses, lessons, progress, and badges, "
        "then reseeds the curriculum and demo student. "
        "In production use `sync_content` instead."
    )

    def handle(self, *args, **options):
        # Curriculum is the only content on the site for now.
        UserBadge.objects.all().delete()
        Progress.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        Skill.objects.all().delete()

        skill, _ = Skill.objects.get_or_create(
            slug=SKILL["slug"],
            defaults={
                "name": SKILL["name"],
                "description": SKILL["description"],
                "order": SKILL["order"],
            },
        )

        for module in CURRICULUM:
            course = Course.objects.create(
                title=module["title"],
                slug=module["slug"],
                description=module["description"],
                skill=skill,
                order=module["order"],
                difficulty=module["difficulty"],
                is_published=module.get("published", True),
            )
            for i, lesson_spec in enumerate(module["lessons"], start=1):
                title, slug, ltype, minutes = lesson_spec[:4]
                config = dict(lesson_spec[4]) if len(lesson_spec) > 4 else {}
                ai_tutor_prompt = config.pop("ai_tutor_prompt", "")
                video_url = (config.pop("video_url", "") or "").strip()
                require_full_watch = bool(config.pop("require_full_watch", True))
                if not config.get("questions"):
                    config["questions"] = default_recap_questions(title, slug)
                Lesson.objects.create(
                    course=course,
                    title=title,
                    slug=slug,
                    lesson_type=ltype,
                    order=i,
                    estimated_minutes=minutes,
                    content=load_content(module["slug"], slug, title),
                    video_url=video_url,
                    require_full_watch=require_full_watch,
                    sandbox_config=config,
                    ai_tutor_prompt=ai_tutor_prompt,
                )

        student, _ = User.objects.get_or_create(
            username="demo_student",
            defaults={"role": User.Role.STUDENT, "email": "demo@agentcraft.dev"},
        )
        student.set_password("demo1234")
        student.save()

        badge_count = seed_badges()
        evaluate_badges_for_user(student)

        self.stdout.write(self.style.SUCCESS("Curriculum seeded (Modules 1–8)."))
        self.stdout.write(f"Modules: {Course.objects.count()} · Lessons: {Lesson.objects.count()}")
        self.stdout.write(f"Badges: {badge_count}")
        self.stdout.write("Login: demo_student / demo1234")
        self.stdout.write(
            "Edit lesson markdown in apps/courses/content/, then run sync_content (prod) "
            "or seed_demo (dev reset)."
        )
