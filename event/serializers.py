from .models import Event, EventCategory
from rest_framework import serializers


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'description', 'start_date', 'end_date',
                  'organization', 'status', 'event_type', 'category', 'event_banner', 'event_dp', "location")


class GetEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'start_date', 'end_date', 'owner', 'organization',
                  'status', 'event_type', 'category', 'event_banner', 'event_dp', 'location', 'address')


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ('name',)


class GetEventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'
