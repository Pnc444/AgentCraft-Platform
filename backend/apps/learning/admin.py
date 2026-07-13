from django.contrib import admin

from .models import Badge, Progress, Recommendation, UserBadge


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "criteria_type", "criteria_value", "order", "is_active"]
    list_filter = ["criteria_type", "is_active"]
    search_fields = ["name", "slug", "description"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order", "name"]


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ["user", "badge", "equipped", "unlocked_at"]
    list_filter = ["equipped", "badge"]
    search_fields = ["user__username", "badge__name"]
    autocomplete_fields = ["user", "badge"]


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ["user", "lesson", "status", "score", "completed_at"]
    list_filter = ["status"]


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ["user", "lesson", "confidence", "is_read"]
    list_filter = ["is_read"]
