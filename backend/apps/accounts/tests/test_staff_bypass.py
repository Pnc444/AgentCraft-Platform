"""The staff bypass: exposed to the client, and not grantable by the client.

The lesson gates live in the browser, so the frontend has to be told whether
an account is staff. That makes `is_staff` a field on a PATCHable endpoint,
which is exactly the shape of an accidental privilege-escalation bug — hence
the tests below.
"""

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APIClient

User = get_user_model()
ME = "/api/v1/auth/me/"


def auth(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def student(db):
    return User.objects.create_user(username="s", password="pw", email="s@example.com")


@pytest.mark.django_db
def test_me_reports_is_staff_so_the_client_can_lift_the_gates(student):
    body = auth(student).get(ME).json()["data"]
    assert body["is_staff"] is False

    student.is_staff = True
    student.save()
    assert auth(student).get(ME).json()["data"]["is_staff"] is True


@pytest.mark.django_db
def test_a_student_cannot_patch_themselves_into_staff(student):
    """The whole reason is_staff is read_only. Staff also opens /admin/, so a
    writable field here would be a privilege escalation, not just free lessons."""
    response = auth(student).patch(ME, {"is_staff": True}, format="json")
    assert response.status_code == 200  # silently ignored, DRF-style
    student.refresh_from_db()
    assert student.is_staff is False


@pytest.mark.django_db
def test_a_student_cannot_put_themselves_into_staff(student):
    auth(student).put(
        ME, {"username": "s", "email": "s@example.com", "is_staff": True}, format="json"
    )
    student.refresh_from_db()
    assert student.is_staff is False


@pytest.mark.django_db
def test_role_stays_read_only_too(student):
    auth(student).patch(ME, {"role": User.Role.AI_INSTRUCTOR}, format="json")
    student.refresh_from_db()
    assert student.role == User.Role.STUDENT


@pytest.mark.django_db
def test_editable_profile_fields_still_work(student):
    """Locking the flags must not lock the fields the profile page edits."""
    auth(student).patch(ME, {"first_name": "Ada"}, format="json")
    student.refresh_from_db()
    assert student.first_name == "Ada"


@pytest.mark.django_db
def test_create_admin_makes_an_account_that_bypasses():
    call_command("create_admin", "--username", "reviewer", "--password", "pw12345678")
    user = User.objects.get(username="reviewer")
    assert user.is_staff and user.is_superuser
    assert user.check_password("pw12345678")
    assert auth(user).get(ME).json()["data"]["is_staff"] is True


@pytest.mark.django_db
def test_create_admin_is_idempotent_and_resets_the_password():
    call_command("create_admin", "--username", "reviewer", "--password", "first12345")
    call_command("create_admin", "--username", "reviewer", "--password", "second12345")
    assert User.objects.filter(username="reviewer").count() == 1
    assert User.objects.get(username="reviewer").check_password("second12345")


@pytest.mark.django_db
def test_staff_only_grants_the_bypass_without_superuser():
    call_command(
        "create_admin", "--username", "r2", "--password", "pw12345678", "--staff-only"
    )
    user = User.objects.get(username="r2")
    assert user.is_staff is True
    assert user.is_superuser is False
