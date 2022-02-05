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
    confirm_password = serializers.CharField(max_length=200)


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
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
    confirm_password = serializers.CharField()
