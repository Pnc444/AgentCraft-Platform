"""Create (or reset) a staff account that bypasses the lesson gates.

`createsuperuser` already does this, but it is interactive and refuses to run
unattended — awkward inside `docker compose exec`, and awkward to repeat when
you have forgotten the password. This is the reviewer's equivalent of
`seed_demo`: one command, idempotent, prints the credentials it just set.

    docker compose exec backend python manage.py create_admin
    docker compose exec backend python manage.py create_admin \
        --username peyton --password 'something better' --email me@example.com
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

User = get_user_model()

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin1234"
DEFAULT_EMAIL = "admin@knightsacademy.dev"


class Command(BaseCommand):
    help = (
        "Create or reset a staff/superuser account. Staff bypass every lesson "
        "gate (module locks, video-before-quiz, beat gating) so content can be "
        "reviewed without playing the course through."
    )

    def add_arguments(self, parser):
        parser.add_argument("--username", default=DEFAULT_USERNAME)
        parser.add_argument("--email", default=DEFAULT_EMAIL)
        parser.add_argument(
            "--password",
            default=DEFAULT_PASSWORD,
            help="Defaults to a well-known development password. Set this for anything reachable.",
        )
        parser.add_argument(
            "--staff-only",
            action="store_true",
            help=(
                "Grant is_staff but not is_superuser. Still bypasses the lesson "
                "gates; does not get blanket permissions in /admin/."
            ),
        )

    def handle(self, *args, **options):
        username = (options["username"] or "").strip()
        password = options["password"] or ""
        if not username:
            raise CommandError("--username cannot be blank")
        if not password:
            raise CommandError("--password cannot be blank")

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": options["email"], "role": User.Role.AI_INSTRUCTOR},
        )
        user.email = options["email"] or user.email
        user.is_staff = True
        # is_staff is what the lesson gates read; is_superuser is what /admin/
        # needs to be useful. Both unless --staff-only says otherwise.
        user.is_superuser = not options["staff_only"]
        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(f"{'Created' if created else 'Updated'} staff account {username!r}")
        )
        self.stdout.write(f"  login:      {username} / {password}")
        self.stdout.write(f"  is_staff:   {user.is_staff}   is_superuser: {user.is_superuser}")
        self.stdout.write("  bypasses:   module locks, video-before-quiz, beat gating, certificate lock")
        self.stdout.write("  django admin: http://localhost:8000/admin/")

        if password == DEFAULT_PASSWORD:
            self.stdout.write(
                self.style.WARNING(
                    "  This is the default development password and it is in the repo. "
                    "Pass --password for anything that is not localhost."
                )
            )
