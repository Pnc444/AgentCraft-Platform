from io import BytesIO
import os

from django.contrib.auth.password_validation import validate_password
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageOps
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from pillow_heif import register_heif_opener

from .models import User

register_heif_opener()

ALLOWED_AVATAR_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/heic",
    "image/heif",
    "image/heic-sequence",
    "image/heif-sequence",
}

# Profile photos are resized and re-encoded to keep storage small.
AVATAR_MAX_EDGE = 512
AVATAR_JPEG_QUALITY = 82


def _compress_avatar(upload) -> InMemoryUploadedFile:
    """Resize to AVATAR_MAX_EDGE and save as optimized JPEG."""
    upload.seek(0)
    with Image.open(upload) as img:
        img = ImageOps.exif_transpose(img)
        img = img.convert("RGB")
        img.thumbnail((AVATAR_MAX_EDGE, AVATAR_MAX_EDGE), Image.Resampling.LANCZOS)
        buffer = BytesIO()
        img.save(
            buffer,
            format="JPEG",
            quality=AVATAR_JPEG_QUALITY,
            optimize=True,
            progressive=True,
        )
    buffer.seek(0)
    base = os.path.splitext(os.path.basename(getattr(upload, "name", "") or "avatar"))[0] or "avatar"
    return InMemoryUploadedFile(
        buffer,
        field_name="avatar",
        name=f"{base}.jpg",
        content_type="image/jpeg",
        size=buffer.getbuffer().nbytes,
        charset=None,
    )


class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Accept username or email in the `username` field (case-insensitive)."""

    def validate(self, attrs):
        login = (attrs.get("username") or "").strip()
        if login:
            if "@" in login:
                user = User.objects.filter(email__iexact=login).first()
            else:
                user = User.objects.filter(username__iexact=login).first()
            if user:
                attrs["username"] = user.get_username()
        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    # FileField (not ImageField) so HEIC can pass through before we convert/compress.
    avatar = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "skill_profile",
            "avatar",
        ]
        read_only_fields = ["id", "username", "role", "skill_profile"]

    def validate_avatar(self, value):
        if value is None:
            return value
        max_bytes = 2 * 1024 * 1024
        if getattr(value, "size", 0) > max_bytes:
            raise serializers.ValidationError("Avatar must be 2MB or smaller.")

        name = (getattr(value, "name", "") or "").lower()
        content_type = (getattr(value, "content_type", "") or "").lower()
        looks_allowed = (
            content_type in ALLOWED_AVATAR_TYPES
            or name.endswith((".jpg", ".jpeg", ".png", ".webp", ".gif", ".heic", ".heif"))
            or not content_type
        )
        if not looks_allowed:
            raise serializers.ValidationError(
                "Use a JPEG, PNG, WebP, GIF, or HEIC image."
            )

        try:
            return _compress_avatar(value)
        except Exception:
            raise serializers.ValidationError("Could not process that image.")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if instance.avatar:
            url = instance.avatar.url
            data["avatar"] = request.build_absolute_uri(url) if request else url
        else:
            data["avatar"] = None
        return data

    def update(self, instance, validated_data):
        request = self.context.get("request")
        clear = False
        if request is not None:
            raw = request.data.get("clear_avatar")
            clear = str(raw).lower() in ("1", "true", "yes")

        if clear:
            if instance.avatar:
                instance.avatar.delete(save=False)
            validated_data["avatar"] = None
        elif "avatar" in validated_data and validated_data["avatar"] is not None:
            if instance.avatar:
                instance.avatar.delete(save=False)

        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm"]

    def validate_username(self, value):
        username = value.strip()
        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return username

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User(role=User.Role.STUDENT, **validated_data)
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
