from rest_framework import serializers
from authentication.models import User


class UserValidator:
    def validate_user_exists(cls, id):
        if not User.objects.filter(id=id).exists():
            raise serializers.ValidationError("User does not exist")
