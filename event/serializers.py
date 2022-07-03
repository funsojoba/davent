from .models import Event, EventCategory, Ticket, CheckIn
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
    name = serializers.CharField(read_only=True)
    owner = UserSerializer(read_only=True)
    participant = UserSerializer(many=True, read_only=True)
    category = EventCategorySerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    description = serializers.CharField(read_only=True)
    start_date = serializers.DateTimeField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)
    event_type = serializers.ChoiceField(choices=Event.TYPE, read_only=True)
    event_banner = serializers.CharField(read_only=True)
    event_dp = serializers.CharField(read_only=True)
    status = serializers.ChoiceField(choices=Event.STATUS, read_only=True)
    location = serializers.ChoiceField(choices=Event.LOCATION, read_only=True)
    address = serializers.CharField(read_only=True)
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


class AdminSetEventStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Event.STATUS)


class UodateEventSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    start_date = serializers.CharField(required=False)
    end_date = serializers.CharField(required=False)
    event_type = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    event_banner = serializers.CharField(required=False)
    event_dp = serializers.CharField(required=False)
    location = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

class TicketSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    event = GetEventSerializer()
    class Meta:
        model = Ticket
        fields = ("status", "event", "owner", "ticket_id", "expiry_date")