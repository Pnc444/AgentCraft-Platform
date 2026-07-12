# Generated manually for Progress.video_watched

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("learning", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="progress",
            name="video_watched",
            field=models.BooleanField(
                default=False,
                help_text="True when the student has finished the lesson video (if any)",
            ),
        ),
    ]
