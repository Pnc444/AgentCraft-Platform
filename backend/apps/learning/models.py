from django.conf import settings
from django.db import models


class Badge(models.Model):
    """Achievement definition shown on the student profile."""

    class Criteria(models.TextChoices):
        LESSONS_COMPLETED = "lessons_completed", "Lessons completed"
        COURSE_COMPLETED = "course_completed", "Course completed"
        PERFECT_QUIZ = "perfect_quiz", "Perfect quiz score"
        PATH_COMPLETE = "path_complete", "Entire learning path complete"

    slug = models.SlugField(unique=True, max_length=80)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon = models.CharField(
        max_length=50,
        help_text="Lucide icon key used by the frontend BadgeIcon map",
    )
    criteria_type = models.CharField(max_length=32, choices=Criteria.choices)
    criteria_value = models.CharField(
        max_length=120,
        blank=True,
        help_text="Threshold (e.g. '1') or course slug for course_completed",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """A badge unlocked by a specific student."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="badges"
    )
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="awards")
    unlocked_at = models.DateTimeField(auto_now_add=True)
    equipped = models.BooleanField(
        default=False,
        help_text="Shown as the student's profile accent badge",
    )

    class Meta:
        unique_together = [["user", "badge"]]
        ordering = ["-unlocked_at"]

    def __str__(self):
        return f"{self.user.username} · {self.badge.name}"


class Progress(models.Model):
    """Tracks a student's progress through lessons."""

    class Status(models.TextChoices):
        NOT_STARTED = "not_started", "Not Started"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        STUCK = "stuck", "Needs Help"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="progress"
    )
    lesson = models.ForeignKey(
        "courses.Lesson", on_delete=models.CASCADE, related_name="progress"
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    score = models.FloatField(null=True, blank=True, help_text="Quiz/assessment score 0-100")
    video_watched = models.BooleanField(
        default=False,
        help_text="True when the student has finished the lesson video (if any)",
    )
    time_spent_minutes = models.PositiveIntegerField(default=0)
    hints_requested = models.PositiveIntegerField(default=0)
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    # Learning signals for the AI instructor:
    interaction_log = models.JSONField(default=list, blank=True)
    # Stores: [{"type": "sandbox_error", "timestamp": ..., "details": ...}, ...]

    class Meta:
        unique_together = [["user", "lesson"]]
        indexes = [models.Index(fields=["user", "status"])]
        verbose_name_plural = "progress records"

    def __str__(self):
        return f"{self.user.username} - {self.lesson} ({self.status})"


class Recommendation(models.Model):
    """AI-generated next-step recommendations for each student."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recommendations"
    )
    lesson = models.ForeignKey("courses.Lesson", on_delete=models.CASCADE)
    reason = models.TextField(blank=True, help_text="Why the AI recommends this next")
    confidence = models.FloatField(default=0.5, help_text="AI confidence 0-1")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-confidence", "-created_at"]

    def __str__(self):
        return f"Recommend {self.lesson} to {self.user.username}"
