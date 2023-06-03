from .models import Event, EventCategory, Ticket, CheckIn
from rest_framework import serializers
from authentication.serializers import UserSerializer
from organization.serializers import OrganizationSerializer

from event.validators import Validator
from authentication.validators import UserValidator


class CreateEventSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[Validator.validate_existing_event])
    event_type = serializers.ChoiceField(choices=Event.TYPE)
    location = serializers.ChoiceField(choices=Event.LOCATION)
    address = serializers.CharField(required=False)
    event_url = serializers.CharField(required=False)
    rsvp = serializers.ListField(required=False, child=serializers.CharField())
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    event_city = serializers.CharField(required=False)
    event_country = serializers.CharField(required=False)
    event_state = serializers.CharField(required=False)
    currency = serializers.CharField(required=False)

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
            "address",
            "event_url",
            "rsvp",
            "amount",
            "event_city",
            "event_country",
            "event_state",
            "currency",
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
            "event_url",
            "rsvp",
            "amount",
            "event_city",
            "event_country",
            "event_state",
            "currency",
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
    event_city = serializers.CharField(required=False)
    event_country = serializers.CharField(required=False)
    event_state = serializers.CharField(required=False)
    rsvp = serializers.JSONField(required=False)
    currency = serializers.CharField(required=False)


class TicketSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    event = serializers.SerializerMethodField()

    def get_event(self, obj):
        return {
            "id": obj.event.id,
            "name": obj.event.name,
            "start_date": obj.event.start_date,
            "end_date": obj.event.end_date,
            "event_type": obj.event.event_type,
            "status": obj.event.status,
            "location": obj.event.location,
            "currency": obj.event.currency,
            "amount": obj.event.amount,
            "address": obj.event.address,
            "event_url": obj.event.event_url,
        }

    class Meta:
        model = Ticket
        fields = ("get_status", "ticket_id", "expiry_date", "event", "owner")


class SendEmailSerializer(serializers.Serializer):
    subject = serializers.CharField()
    message = serializers.CharField()
    link = serializers.CharField(required=False)
    link_text = serializers.CharField(required=False)
