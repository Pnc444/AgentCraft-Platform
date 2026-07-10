from django.contrib import admin

from .models import Progress, Recommendation


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ["user", "lesson", "status", "score", "completed_at"]
    list_filter = ["status"]


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ["user", "lesson", "confidence", "is_read"]
    list_filter = ["is_read"]
