from django.conf import settings
from django.db import models


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
