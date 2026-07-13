from django.db import migrations


def seed_badge_catalog(apps, schema_editor):
    from apps.learning.badges import seed_badges

    seed_badges()


def clear_badges(apps, schema_editor):
    Badge = apps.get_model("learning", "Badge")
    Badge.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("learning", "0003_badge_models"),
    ]

    operations = [
        migrations.RunPython(seed_badge_catalog, clear_badges),
    ]
