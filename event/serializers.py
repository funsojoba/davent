from .models import Event, EventCategory
from rest_framework import serializers
from authentication.serializers import UserSerializer
from organization.serializers import OrganizationSerializer


class CreateEventSerializer(serializers.ModelSerializer):
    event_type = serializers.ChoiceField(choices=Event.TYPE)
    location = serializers.ChoiceField(choices=Event.LOCATION)

    class Meta:
        model = Event
        fields = (
            "name",
            "description",
            "start_date",
            "end_date",
            "organization",
            "status",
            "event_type",
            "category",
            "event_banner",
            "event_dp",
            "location",
        )


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ("id", "name")


class GetEventSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    participant = UserSerializer(many=True)
    category = EventCategorySerializer()
    organization = OrganizationSerializer()

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "owner",
            "organization",
            "participant",
            "status",
            "event_type",
            "category",
            "event_banner",
            "event_dp",
            "location",
            "address",
        )


class GetEventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = "__all__"


class AdminRegisterUserSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.CharField())
