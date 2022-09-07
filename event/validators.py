from rest_framework import serializers

from event.models import Event


class Validator:
    @classmethod
    def validate_existing_event(cls, name):
        if Event.objects.filter(name__iexact=name).exists():
            raise serializers.ValidationError("name of event already exists")
