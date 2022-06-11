from typing import List
from django.db import transaction
from rest_framework import status
from helpers.response import Response
from helpers.permissions import IsAdminUser, IsUser

from .models import Event, EventCategory
from . import serializers
from organization.service import OrganizationService
from authentication.service import UserService


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
        event_category = EventCategoryService.get_event_category(
            user=user, id=kwargs.get("category")
        )
        organization = OrganizationService.get_organization(
            id=kwargs.get("organization")
        )

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
            address=kwargs.get("address", ""),
        )

    @classmethod
    def get_events(cls, **kwargs):
        return Event.objects.filter(**kwargs).all()

    @classmethod
    def get_event_participants(cls, user, event_id):
        event = Event.objects.filter(owner=user, id=event_id).first()
        return event.participant.all()

    @classmethod
    def register_event(cls, user, event_id):
        event = Event.objects.filter(id=event_id).first()
        event.participant.add(user)
        event.save()
        return event

    @classmethod
    def get_single_event(cls, **kwargs):
        return Event.objects.filter(**kwargs).first()

    @classmethod
    def admin_register_user(cls, user_ids: List[str], event_id):
        """
        this service allows an admin registers multiple users for an event
        """
        # TODO: find a way to limit entries to maybe 10 at ones
        event = cls.get_single_event(id=event_id)
        with transaction.atomic():
            for user_id in user_ids:
                user = UserService.get_user(id=user_id)
                event.participant.add(user)
        return event
