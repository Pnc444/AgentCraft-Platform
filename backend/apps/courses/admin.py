from django.contrib import admin

from .models import Course, Lesson, Skill


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "skill", "difficulty", "is_published"]
    list_filter = ["is_published", "difficulty", "skill"]
    prepopulated_fields = {"slug": ["title"]}
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "lesson_type", "order", "estimated_minutes"]
    list_filter = ["lesson_type", "course"]
