from django.contrib import admin

from .models import Course, Lesson, Skill


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1
    show_change_link = True
    fields = (
        "title",
        "slug",
        "lesson_type",
        "order",
        "estimated_minutes",
        "video_url",
        "require_full_watch",
        "content",
        "sandbox_config",
    )
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order"]
    search_fields = ["name", "slug"]
    ordering = ["order", "name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "skill", "order", "difficulty", "is_published"]
    list_filter = ["is_published", "difficulty", "skill"]
    search_fields = ["title", "slug", "description"]
    ordering = ["order"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["prerequisites"]
    inlines = [LessonInline]
    fieldsets = (
        (None, {"fields": ("title", "slug", "description", "skill", "order", "difficulty")}),
        ("Publishing", {"fields": ("is_published", "prerequisites")}),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "course",
        "lesson_type",
        "order",
        "estimated_minutes",
        "has_video",
    ]
    list_filter = ["lesson_type", "course"]
    search_fields = ["title", "slug", "content", "course__title"]
    ordering = ["course__order", "order"]
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["course"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "course",
                    "title",
                    "slug",
                    "lesson_type",
                    "order",
                    "estimated_minutes",
                )
            },
        ),
        (
            "Content",
            {
                "fields": ("content",),
                "description": "Write lesson body in Markdown. Students see this on the lesson page.",
            },
        ),
        (
            "Video (optional)",
            {
                "fields": ("video_url", "require_full_watch"),
                "description": (
                    "Paste a YouTube watch, youtu.be, or embed link. "
                    "When set, students get a Video tab in the lesson (16:9 player). "
                    "Use “Require full watch” to lock the Recap Quiz until they finish the video, "
                    "or uncheck it to let them skip."
                ),
            },
        ),
        (
            "Quiz / sandbox config",
            {
                "fields": ("sandbox_config",),
                "classes": ("collapse",),
                "description": (
                    'For quizzes, use JSON like: '
                    '{"questions":[{"id":"q1","prompt":"...","options":["A","B"],"answer_index":0}]}'
                ),
            },
        ),
        (
            "AI tutor",
            {
                "fields": ("ai_tutor_prompt",),
                "classes": ("collapse",),
            },
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.display(boolean=True, description="Video")
    def has_video(self, obj):
        return bool(obj.video_url)
