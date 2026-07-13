# Generated manually for Lesson.require_full_watch

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0003_lesson_video_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="require_full_watch",
            field=models.BooleanField(
                default=True,
                help_text=(
                    "If enabled, students must watch the video to the end before the Recap Quiz "
                    "unlocks. Turn off to let them skip the video."
                ),
            ),
        ),
    ]
