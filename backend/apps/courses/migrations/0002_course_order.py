# Generated manually for curriculum order support

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="order",
            field=models.PositiveIntegerField(
                default=0, help_text="Display order in the curriculum sidebar"
            ),
        ),
        migrations.AlterModelOptions(
            name="course",
            options={"ordering": ["order", "skill__order", "title"]},
        ),
    ]
