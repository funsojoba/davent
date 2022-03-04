from .models import Event, EventCategory
from rest_framework import serializers


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'description', 'start_date', 'end_date', 'owner', 'participant',
                  'organization', 'status', 'event_type', 'category', 'event_banner', 'event_dp')


class GetEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ('name', 'owner')


class GetEventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'

