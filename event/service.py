from typing import List
from django.db import transaction
from rest_framework import status
from helpers.response import Response
from helpers.permissions import IsAdminUser, IsUser
from helpers.random_string import random_string
from helpers.exception import CustomApiException

from .models import Event, EventCategory, Ticket, CheckIn
from . import serializers

from authentication.service import UserService
from notification.service import EmailService

from helpers.response import Response


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
        from organization.service import OrganizationService

        event_category = EventCategoryService.get_event_category(
            user=user, id=kwargs.get("category")
        )
        organization = OrganizationService.get_organization(
            id=kwargs.get("organization")
        )
        event_type = kwargs.get("event_type")

        if event_type.lower() == "paid" and kwargs.get("amount") is None:
            raise CustomApiException(
                detail="Amount is required for paid event",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if kwargs.get("location").lower() == "onsite" and not kwargs.get("address"):
            raise CustomApiException(
                "address is required for on-site event",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return Event.objects.create(
            name=kwargs.get("name"),
            description=kwargs.get("description"),
            start_date=kwargs.get("start_date"),
            end_date=kwargs.get("end_date"),
            organization=organization,
            owner=user,
            status=kwargs.get("status"),
            event_type=event_type.upper(),
            category=event_category,
            event_banner=kwargs.get("event_banner", ""),
            event_dp=kwargs.get("event_dp", ""),
            location=kwargs.get("location"),
            address=kwargs.get("address", ""),
            event_url=kwargs.get("event_url"),
            rsvp=kwargs.get("rsvp"),
            amount=kwargs.get("amount"),
            event_city=kwargs.get("event_city"),
            event_country=kwargs.get("event_country"),
            event_state=kwargs.get("event_state"),
            currency=kwargs.get("currency", "NGN"),
        )

    @classmethod
    def get_events(cls, **kwargs):
        return Event.objects.filter(**kwargs).all()

    @classmethod
    def get_event_participants(cls, user, event_id):
        event = Event.objects.filter(owner=user, id=event_id).first()
        return event.participant.all()

    @classmethod
    def generate_event_ticket(cls, event, user, status, expiry_date):
        """
        This method generates event ticket for user in background
        """
        from event.tasks import generate_ticket_async

        # create ticket for a user for an event
        ticket = generate_ticket_async.delay(event, user, status, expiry_date)

    @classmethod
    def register_event(cls, user, event_id):
        """
        This method allows a user register for an event
        """
        event = Event.objects.filter(id=event_id).first()
        event.participant.add(user)
        event.save()

        cls.generate_event_ticket(
            event, user, status="ACTIVE", expiry_date=event.start_date
        )
        return event

    @classmethod
    def get_single_event(cls, **kwargs):
        return Event.objects.filter(**kwargs).first()

    @classmethod
    def admin_register_user(cls, user_ids: List[str], event_id):
        """
        this service allows an admin registers multiple users for an event
        """
        if len(user_ids) > 10:
            pass
        event = cls.get_single_event(id=event_id)
        with transaction.atomic():
            for user_id in user_ids:
                user = UserService.get_user(id=user_id)
                if not user:
                    continue
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

    @classmethod
    def send_email_to_users(
        cls, event_id, user, subject, message, link: str = None, link_text: str = None
    ):
        event = cls.get_single_event(id=event_id)
        users = event.participant.all()

        user_emails = [user.email for user in users]
        context = {
            "event_name": event.name,
            "message": message,
            "link": link,
            "link_text": link_text,
        }

        # TODO: this is throwing template not found error
        EmailService.send_async(
            template="user_event_alert.html",
            subject=subject,
            recipients=user_emails,
            context=context,
        )
        return Response(
            {"message": "Email sent successfully"}, status=status.HTTP_200_OK
        )


class CheckInService:
    @classmethod
    def check_in(cls, event, user):
        check_in = CheckIn.object.create(event=event, user=user)


class TicketService:
    @classmethod
    def create_ticket(cls, event, user, status, expiry_date):
        ticket_id = random_string(11)
        return Ticket.objects.create(
            event=event,
            owner=user,
            ticket_id=ticket_id,
            status=status,
            expiry_date=expiry_date,
        )

    @classmethod
    def get_ticket(cls, user, event_id):
        event = EventService.get_single_event(id=event_id)
        return Ticket.objects.filter(owner=user, event=event).first()

    @classmethod
    def list_tickets(cls, **kwargs):
        return Ticket.objects.filter(**kwargs)

    @classmethod
    def list_event_tickets(cls, event_id):
        event = EventService.get_single_event(id=event_id)
        return Ticket.objects.filter(event=event)

    @classmethod
    def verify_ticket_status(cls, ticket_id, event_id):
        ticket = cls.get_ticket(id=ticket_id)
        event = EventService.get_single_event(id=event_id)

        # TODO: this code has not been tested oo
        # and I'm not sure of this logic seff
        if ticket.event.start_date > event.start_date:
            ticket.status = "EXPIRED"
            ticket.save()
            return {"status": False, "message": "Ticket has expired"}
        return {"status": True, "message": "Ticket is valid"}

    @classmethod
    def invalidate_ticket(cls, ticket_id):
        ticket = cls.get_ticket(id=ticket_id)
        ticket.status = "INVALID"
        ticket.save()
        return ticket

    @classmethod
    def verify_ticket(cls, ticket_number):
        # TODO: Find a way to ensure the ticket number will always be unique
        ticket = Ticket.objects.filter(ticket_id=ticket_number).first()
        return True if ticket else False


class EventPaymetService:
    @classmethod
    def create_event_payment(cls, event_id):
        event = EventService.get_single_event(id=event_id)

        if event.event_type == "PAID":
            EventPayment.objects.create(event=event, status="PENDING")
