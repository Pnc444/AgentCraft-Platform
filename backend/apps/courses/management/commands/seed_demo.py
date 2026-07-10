from django.core.management.base import BaseCommand

from apps.accounts.models import User
from apps.courses.models import Course, Lesson, Skill
from apps.learning.models import Progress


class Command(BaseCommand):
    help = "Seed demo data for MVP demo"

    def handle(self, *args, **options):
        skills_data = [
            ("AI Literacy", "ai-literacy", "Understand what AI can and cannot do", 1),
            ("Terminal", "terminal", "Command line basics", 2),
            ("Git", "git", "Version control with Git", 3),
            ("Python", "python", "Programming fundamentals", 4),
            ("Docker", "docker", "Containers and environments", 5),
            ("AI Agents", "ai-agents", "Build intelligent agents", 6),
        ]
        skills = {}
        for name, slug, desc, order in skills_data:
            skill, _ = Skill.objects.get_or_create(
                slug=slug, defaults={"name": name, "description": desc, "order": order}
            )
            skills[slug] = skill

        courses_data = [
            ("AI Literacy Fundamentals", "ai-literacy-fundamentals", "What AI is, isn't, and what it means for you", "ai-literacy", 1),
            ("Terminal Basics", "terminal-basics", "Navigate the command line with confidence", "terminal", 1),
            ("Git Basics", "git-basics", "Track code, collaborate, and never lose work", "git", 1),
            ("Python Fundamentals", "python-fundamentals", "Write your first programs", "python", 1),
            ("Docker Basics", "docker-basics", "Package and run apps in containers", "docker", 2),
            ("AI Agent Lab", "ai-agent-lab", "Build your first AI agent from scratch", "ai-agents", 3),
        ]
        lesson_titles = {
            "ai-literacy-fundamentals": [("What Can AI Do?", "theory", 5), ("Try an AI Model", "interactive", 10), ("What AI Can't Do", "theory", 5)],
            "terminal-basics": [("Your First Command", "interactive", 7), ("Navigating Folders", "interactive", 7), ("Files & Shortcuts", "interactive", 6)],
            "git-basics": [("Why Version Control?", "theory", 5), ("Init a Repo", "interactive", 10), ("Commit & Push", "interactive", 10)],
            "python-fundamentals": [("Hello World", "interactive", 10), ("Variables & Types", "interactive", 10), ("Loops & Conditions", "interactive", 10)],
            "docker-basics": [("What is a Container?", "theory", 10), ("Your First Container", "sandbox", 15), ("Dockerfiles", "sandbox", 10)],
            "ai-agent-lab": [("Agent Architecture", "theory", 10), ("Build the Brain", "agent_lab", 20), ("Test Your Agent", "agent_lab", 15)],
        }
        for title, slug, desc, skill_slug, difficulty in courses_data:
            course, created = Course.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "description": desc,
                    "skill": skills[skill_slug],
                    "difficulty": difficulty,
                    "is_published": True,
                },
            )
            if created:
                for i, (ltitle, ltype, lmin) in enumerate(lesson_titles.get(slug, []), 1):
                    Lesson.objects.get_or_create(
                        course=course,
                        slug=f"lesson-{i}",
                        defaults={
                            "title": ltitle,
                            "lesson_type": ltype,
                            "order": i,
                            "estimated_minutes": lmin,
                            "content": f"# {ltitle}\n\nThis lesson content will be written by Preston's curriculum team.",
                        },
                    )

        student, _ = User.objects.get_or_create(
            username="demo_student",
            defaults={"role": User.Role.STUDENT, "email": "demo@agentcraft.dev"},
        )
        student.set_password("demo1234")
        student.save()

        for lesson in Lesson.objects.all()[:4]:
            Progress.objects.get_or_create(
                user=student,
                lesson=lesson,
                defaults={
                    "status": Progress.Status.COMPLETED,
                    "score": 85,
                    "time_spent_minutes": lesson.estimated_minutes,
                },
            )

        self.stdout.write(self.style.SUCCESS("Demo data seeded!"))
        self.stdout.write("Login: demo_student / demo1234")
