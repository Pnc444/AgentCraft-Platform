from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Knight's Academy", {"fields": ("role", "skill_profile", "avatar")}),)
    list_display = ["username", "email", "role", "is_staff"]
