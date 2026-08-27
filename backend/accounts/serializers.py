"""
accounts/serializers.py

All serializers for the accounts app.
Backend validation is always enforced regardless of frontend checks.
"""

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, UserRole


# ── Custom JWT payload ─────────────────────────────────────────────────────────

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extends the default JWT claim with user role and full_name.
    Referenced in settings: SIMPLE_JWT['TOKEN_OBTAIN_SERIALIZER'].
    """

    def validate(self, attrs):
        # Check that the user is active before issuing tokens.
        # SimpleJWT uses USERNAME_FIELD ("email") as the attrs key.
        email = attrs.get(self.username_field, "")
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                raise serializers.ValidationError(
                    "Email address not verified. Please check your inbox."
                )
        except User.DoesNotExist:
            pass  # Let the parent handle the invalid credentials error

        data = super().validate(attrs)
        data["user"] = UserProfileSerializer(self.user).data
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["full_name"] = user.full_name
        token["email"] = user.email
        return token


# ── Registration ───────────────────────────────────────────────────────────────

ALLOWED_ROLES = {UserRole.CUSTOMER, UserRole.RESTAURANT, UserRole.RIDER}


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=[r.value for r in ALLOWED_ROLES])

    class Meta:
        model = User
        fields = ["email", "full_name", "phone", "role", "password", "password_confirm"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value.lower()

    def validate_role(self, value):
        if value == UserRole.ADMIN:
            raise serializers.ValidationError("Cannot register as admin.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False  # activated on email verify
        user.save()
        return user


# ── Email Verification ─────────────────────────────────────────────────────────

class EmailVerifySerializer(serializers.Serializer):
    token = serializers.UUIDField()


# ── Password Reset ─────────────────────────────────────────────────────────────

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(validators=[validate_password], write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password_confirm": "Passwords do not match."}
            )
        return attrs


# ── User Profile ───────────────────────────────────────────────────────────────

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "phone", "role", "is_active", "created_at"]
        read_only_fields = ["id", "email", "role", "is_active", "created_at"]
