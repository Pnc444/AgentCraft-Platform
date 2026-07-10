from rest_framework import serializers

from apps.learning.models import Progress

from .models import Course, Lesson, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "slug", "description", "order"]


class LessonListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ["id", "title", "slug", "lesson_type", "order", "estimated_minutes", "status"]

    def get_status(self, obj):
        progress_map = self.context.get("progress_map", {})
        return progress_map.get(obj.id, Progress.Status.NOT_STARTED)


class LessonDetailSerializer(LessonListSerializer):
    course_slug = serializers.CharField(source="course.slug", read_only=True)
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta(LessonListSerializer.Meta):
        fields = LessonListSerializer.Meta.fields + [
            "content",
            "sandbox_config",
            "course_slug",
            "course_title",
        ]


class CourseListSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    total_lessons = serializers.IntegerField(read_only=True, default=0)
    completed_lessons = serializers.IntegerField(read_only=True, default=0)
    total_minutes = serializers.IntegerField(read_only=True, default=0)
    completion_pct = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "skill",
            "difficulty",
            "total_lessons",
            "completed_lessons",
            "total_minutes",
            "completion_pct",
        ]

    def get_completion_pct(self, obj):
        total = getattr(obj, "total_lessons", 0) or 0
        completed = getattr(obj, "completed_lessons", 0) or 0
        return round(completed / total * 100) if total else 0


class CourseDetailSerializer(CourseListSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta(CourseListSerializer.Meta):
        fields = CourseListSerializer.Meta.fields + ["lessons"]

    def get_lessons(self, obj):
        return LessonListSerializer(obj.lessons.all(), many=True, context=self.context).data
