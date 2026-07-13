from django.db import models


class Skill(models.Model):
    """A skill node in the learning map (e.g. Git, Python, Docker, AI Agents)."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order in skill map")

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "skills"

    def __str__(self):
        return self.name


class CourseQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def with_progress(self, user):
        """Annotate courses with the user's lesson completion counts."""
        from apps.learning.models import Progress

        return self.annotate(
            total_lessons=models.Count("lessons", distinct=True),
            completed_lessons=models.Count(
                "lessons",
                filter=models.Q(
                    lessons__progress__user=user,
                    lessons__progress__status=Progress.Status.COMPLETED,
                ),
                distinct=True,
            ),
            total_minutes=models.Sum("lessons__estimated_minutes"),
        )


class Course(models.Model):
    """A course groups related lessons (e.g. Git Basics, Docker Fundamentals)."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="courses")
    order = models.PositiveIntegerField(
        default=0, help_text="Display order in the curriculum sidebar"
    )
    difficulty = models.PositiveSmallIntegerField(
        default=1, help_text="1=beginner, 2=intermediate, 3=advanced"
    )
    prerequisites = models.ManyToManyField(
        "self", blank=True, symmetrical=False, help_text="Courses that should be completed first"
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CourseQuerySet.as_manager()

    class Meta:
        ordering = ["order", "skill__order", "title"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """A single 5-15 minute interactive lesson."""

    class LessonType(models.TextChoices):
        THEORY = "theory", "Theory"
        INTERACTIVE = "interactive", "Interactive"
        SANDBOX = "sandbox", "Sandbox Practical"
        QUIZ = "quiz", "Quiz"
        AGENT_LAB = "agent_lab", "AI Agent Lab"

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = models.TextField(blank=True, help_text="Markdown lesson content/instructions")
    video_url = models.URLField(
        blank=True,
        help_text="Optional YouTube watch, youtu.be, or embed URL (shown in a 16:9 player)",
    )
    require_full_watch = models.BooleanField(
        default=True,
        help_text=(
            "If enabled, students must watch the video to the end before the Recap Quiz unlocks. "
            "Turn off to let them skip the video."
        ),
    )
    lesson_type = models.CharField(
        max_length=30, choices=LessonType.choices, default=LessonType.THEORY
    )
    order = models.PositiveIntegerField(default=0)
    estimated_minutes = models.PositiveSmallIntegerField(default=10)
    sandbox_config = models.JSONField(
        default=dict,
        blank=True,
        help_text="Docker image, port, startup command for sandbox lessons",
    )
    ai_tutor_prompt = models.TextField(
        blank=True, help_text="System prompt snippet for the AI tutor on this lesson"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        unique_together = [["course", "slug"]]

    def __str__(self):
        return f"{self.course.title} -> {self.title}"
