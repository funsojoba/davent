from typing import List
from django.db import transaction
from rest_framework import status
from helpers.response import Response
from helpers.permissions import IsAdminUser, IsUser

from .models import Event, EventCategory, Ticket, CheckIn
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
    def generate_event_ticket(cls, event, user):
        pass

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

    @classmethod
    def admin_set_event_status(cls, event_id, status):
        event = cls.get_single_event(id=event_id)
        event.status = status
        event.save()
        return event

    @classmethod
    def update_event(cls, event_id, owner, **kwargs):
        event = cls.get_single_event(id=event_id, owner=owner)

        # TODO: this kinda looks redundant though
        event.name = kwargs.get("name") or event.name
        event.description = kwargs.get("description") or event.description
        event.start_date = kwargs.get("start_date") or event.start_date
        event.end_date = kwargs.get("end_date") or event.end_date
        event.event_type = kwargs.get("event_type") or event.event_type
        event.category = (
            EventCategoryService.get_event_category(
                user=owner, id=kwargs.get("category")
            )
            or event.category
        )
        event.event_banner = kwargs.get("event_banner") or event.event_banner
        event.event_dp = kwargs.get("event_dp") or event.event_dp
        event.location = kwargs.get("location") or event.location
        event.address = kwargs.get("address") or event.address

        event.save()
        return event


class CheckInService:
    @classmethod
    def check_in(cls, event, user):
        check_in = CheckIn.object.create(event=event, user=user)
