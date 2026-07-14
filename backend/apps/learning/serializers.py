from rest_framework import serializers

from .models import Progress, Recommendation


class ProgressUpdateSerializer(serializers.ModelSerializer):
    interaction_event = serializers.JSONField(required=False, write_only=True)

    class Meta:
        model = Progress
        fields = ["status", "score", "time_spent_minutes", "video_watched", "interaction_event"]

    def validate_interaction_event(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("interaction_event must be an object.")

        event_type = value.get("type")
        key = value.get("key")
        if not isinstance(event_type, str) or not event_type.strip():
            raise serializers.ValidationError("interaction_event.type is required.")
        if not isinstance(key, str) or not key.strip():
            raise serializers.ValidationError("interaction_event.key is required.")

        status = value.get("status")
        if status is not None and (not isinstance(status, str) or not status.strip()):
            raise serializers.ValidationError("interaction_event.status must be a non-empty string when provided.")

        details = value.get("details")
        if details is not None and not isinstance(details, dict):
            raise serializers.ValidationError("interaction_event.details must be an object when provided.")

        return value


class ProgressSerializer(serializers.ModelSerializer):
    lesson_id = serializers.IntegerField(source="lesson.id", read_only=True)

    class Meta:
        model = Progress
        fields = [
            "lesson_id",
            "status",
            "score",
            "time_spent_minutes",
            "video_watched",
            "completed_at",
            "interaction_log",
        ]


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
