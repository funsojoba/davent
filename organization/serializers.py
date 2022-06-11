from .models import Organization
from rest_framework import serializers
from authentication.serializers import UserSerializer


class OrganizationSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Organization
        fields = ("id", "owner", "name", "description", "category", "members")


class CreateOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("name", "description", "category")


class UpdateOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("name", "description", "category")
