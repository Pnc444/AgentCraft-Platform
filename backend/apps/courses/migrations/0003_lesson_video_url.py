# Generated manually for Lesson.video_url

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0002_course_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="video_url",
            field=models.URLField(
                blank=True,
                help_text="Optional YouTube watch, youtu.be, or embed URL (shown in a 16:9 player)",
            ),
        ),
    ]
