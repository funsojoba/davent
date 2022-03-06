from rest_framework import status
from helpers.response import Response
from helpers.permissions import IsAdminUser, IsUser

from .models import Event, EventCategory
from . import serializers
from organization.service import OrganizationService


class EventCategoryService:
    @classmethod
    def get_event_category(cls, user, **kwargs):
        return EventCategory.objects.filter(owner=user, **kwargs).first()

    @classmethod
    def list_event_category(cls, user):
        return EventCategory.objects.filter(owner=user)
    
    @classmethod
    def create_event_category(cls, user, **kwargs):
        return EventCategory.objects.create(owner=user, name=kwargs.get("name"))
class EventService:
    @classmethod
    def create_event(cls, user, **kwargs):
        event_category = EventCategoryService.get_event_category(user=user, id=kwargs.get("category"))
        organization = OrganizationService.get_organization(id=kwargs.get("organization"))
        
        return Event.objects.create(
            name=kwargs.get("name"),
            description=kwargs.get("description"),
            start_date=kwargs.get("start_date"),
            end_date=kwargs.get("end_date"),
            owner=user,
            status=kwargs.get("status"),
            event_type=kwargs.get("event_type"),
            event_banner=kwargs.get("event_banner", ""),
            event_dp=kwargs.get("event_dp", ""),
            organization=organization,
            category=event_category,
            location=kwargs.get("location"),
            address=kwargs.get("address", "")
        )
        
    @classmethod
    def get_events(cls, **kwargs):
        return Event.objects.filter(**kwargs)

    @classmethod
    def register_event(cls, user, event_id):
        event = Event.objects.filter(id=event_id).first()
        event.participant.add(user)
        event.save()
        return event