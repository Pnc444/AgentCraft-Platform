from rest_framework import serializers

from .models import Progress, Recommendation


class ProgressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ["status", "score", "time_spent_minutes"]


class ProgressSerializer(serializers.ModelSerializer):
    lesson_id = serializers.IntegerField(source="lesson.id", read_only=True)

    class Meta:
        model = Progress
        fields = ["lesson_id", "status", "score", "time_spent_minutes", "completed_at"]


class RecommendationSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source="lesson.title", read_only=True)
    lesson_slug = serializers.CharField(source="lesson.slug", read_only=True)
    course_title = serializers.CharField(source="lesson.course.title", read_only=True)
    course_slug = serializers.CharField(source="lesson.course.slug", read_only=True)

    class Meta:
        model = Recommendation
        fields = [
            "id",
            "reason",
            "confidence",
            "is_read",
            "lesson_title",
            "lesson_slug",
            "course_title",
            "course_slug",
        ]
