from rest_framework import serializers
from .models import User


class RegisterUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=200)
    city = serializers.CharField(max_length=200)
    state = serializers.CharField(max_length=200)
    country = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError(detail="User with email already exist.")
        self.user = user.first()
        return value


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "city",
            "state",
            "country",
            "user_type",
            "avatar",
        )


class VerifyAccountSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=8)
    email = serializers.EmailField()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    email = serializers.EmailField()
    code = serializers.CharField()


class VerifyResetPassword(serializers.Serializer):
    code = serializers.CharField()
    email = serializers.EmailField()


class UpdateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=200, required=None)
    last_name = serializers.CharField(max_length=200, required=None)
    email = serializers.CharField(max_length=200, required=None)
    phone_number = serializers.CharField(max_length=200, required=None)
    city = serializers.CharField(max_length=200, required=None)
    state = serializers.CharField(max_length=200, required=None)
    country = serializers.CharField(max_length=200, required=None)
    avatar = serializers.CharField(max_length=200, required=None)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "city",
            "state",
            "country",
            "avatar",
        )


class UserAvatarSerializer(serializers.Serializer):
    avatar = serializers.FileField()
