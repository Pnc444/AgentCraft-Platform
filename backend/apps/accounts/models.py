from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        AI_INSTRUCTOR = "ai_instructor", "AI Instructor"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    skill_profile = models.JSONField(default=dict, blank=True)
    # skill_profile stores: {"git": 0.3, "python": 0.1, "docker": 0.0, ...}
