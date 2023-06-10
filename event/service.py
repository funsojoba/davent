from typing import List
from django.db import transaction
from django.db.models import F, Q
from django.http import Http404

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

        event_created = Event.objects.create(
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
            amount=kwargs.get("amount", 0),
            event_city=kwargs.get("event_city"),
            event_country=kwargs.get("event_country"),
            event_state=kwargs.get("event_state"),
            currency=kwargs.get("currency", "NGN"),
            participant_capacity=kwargs.get("participant_capacity", 0),
            remaining_slots=kwargs.get("participant_capacity", 0),
        )
        context = {
            "organization_name": organization.name,
            "event_name": event_created.name,
            "event_date": event_created.start_date,
            "event_type": event_created.event_type,
            "event_location": event_created.location,
            "event_url": f"https://www.davent.come/event/{event_created.id}",
            "event_address": event_created.address if event_created.address else None,
            "rsvp": event_created.rsvp,
        }
        EmailService.send_async(
            "admin_event_creation.html",
            "Event Creation",
            [user.email],
            context=context,
        )
        return event_created

    @classmethod
    def get_events(cls, **kwargs):
        return Event.objects.filter(**kwargs).all()

    @classmethod
    def get_event_participants(cls, user, event_id):
        event = Event.objects.filter(owner=user, id=event_id).first()
        return event.participant.all()

    @classmethod
    def generate_event_ticket(cls, event_id, user_id, status, expiry_date):
        """
        This method generates event ticket for user in background
        """
        from event.tasks import generate_ticket_async

        # create ticket for a user for an event
        ticket = generate_ticket_async.delay(event_id, user_id, status, expiry_date)

    @classmethod
    def register_event_free(cls, user, event_id, amount=None):
        """
        This method allows a user register for an event
        """
        event = Event.objects.filter(id=event_id).first()
        if event.participant.all().filter(id=user.id).exists():
            raise CustomApiException(
                detail="You have already registered for this event",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if event.event_type == "PAID":
            raise CustomApiException(
                detail="This event is not free", status_code=status.HTTP_400_BAD_REQUEST
            )

        context = {
            "event_name": event.name,
            "event_date": event.start_date,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "event_type": event.event_type,
            "event_location": event.location,
            "event_address": event.address,
            "participant_city": user.city,
            "participant_state": user.state,
            "event_url": f"https://www.davent.com/event/{event.id}",
            "ticket_link": "https://www.davent.com/event/1e832oise",
            "rsvp": ", ".join(event.rsvp) if event.rsvp else None,
        }

        if event.participant_capacity != 0:
            # NOTE: Handling for race condition
            with transaction.atomic():
                # Fetch the event again within the transaction to ensure consistent data
                event = Event.objects.select_for_update().filter(id=event_id).first()

                if event.participant.all().count() >= event.participant_capacity:
                    raise CustomApiException(
                        detail="This event is sold out",
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )

                event.remaining_slots = F("remaining_slots") - 1
                event.participant.add(user)
                event.save()

                context["participant_count"] = event.participant.count()
                EmailService.send_async(
                    "user_event_registration.html",
                    "Event Registration",
                    [user.email],
                    context=context,
                )

                # Send email to the event admin (event owner)
                EmailService.send_async(
                    "admin_event_registration.html",
                    "Event Registration",
                    [event.owner.email],
                    context=context,
                )
        else:
            event.participant.add(user)
            event.save()
            context["participant_count"] = event.participant.count()

            # TODO: Move this to generate_ticket task when PDF ticket is figured out, same for the paid event above
            EmailService.send_async(
                "user_event_registration.html",
                "Event Registration",
                [user.email],
                context=context,
            )

            # Send email to the event admin (event owner)
            EmailService.send_async(
                "admin_event_registration.html",
                "Event Registration",
                [event.owner.email],
                context=context,
            )

        cls.generate_event_ticket(
            event.id, user.id, status="ACTIVE", expiry_date=event.start_date
        )
        return event

    @classmethod
    def get_single_event(cls, **kwargs):
        return Event.objects.filter(**kwargs).first()

    @classmethod
    def get_registered_event(cls, user):
        """_summary_

        This method gets a list of events a user has registered for

        Args:
            user : user instance

        Returns:
            <list>: list of events
        """
        return Event.objects.filter(participant=user)

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
        """this method allows event admin manually set the status of an event to either ACTIVE, EXPIRED or SCHEDULED

        Args:
            event_id ([str]): event's ID
            status ([str]): [ACTIVE, EXPIRED, SCHEDULED]

        Returns:
            [type]: updated event instance
        """
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
        event.event_city = kwargs.get("event_city") or event.event_city
        event.event_country = kwargs.get("event_country") or event.event_country
        event.event_state = kwargs.get("event_state") or event.event_state
        event.rsvp = kwargs.get("rsvp") or event.rsvp
        event.currency = kwargs.get("currency") or event.currency

        event.save()
        return event

    @classmethod
    def send_email_to_users(cls, event_id, subject, message, link: str = None):
        """This method allows event admin send an email to all participant of an event
            as opposed the automated ones in cases where a piece of information needs to be passed

        Args:
            event_id ([str]): event's ID
            subject ([str]): email subject
            message ([str]): email message
            link (str, optional): [str / url]. Defaults to None.

        Returns:
            None: if success, email sent
        """
        event = cls.get_single_event(id=event_id)
        users = event.participant.all()

        user_emails = [user.email for user in users]
        context = {
            "event_name": event.name,
            "message": message,
            "link": link,
            "link_text": link,
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
    def check_in(cls, admin, event, check_type, query):
        """This function allows admin check in users of an event

        Args:
            event ([type]): event instance
            query ([str]): any of user's email, phone, first or last name
            check_type ([str]): CHECK_IN or CHECK_OUT

        Returns:
            [CheckIn]: CheckIn instance or 404 if user is not found
        """
        user = (
            UserService.get_all_users()
            .filter(
                Q(phone_number=query)
                | Q(email=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
            )
            .first()
        )
        if user:
            # Check if user is registered for the event
            if event.participant.filter(email=user.email).exists():
                return CheckIn.objects.create(
                    event=event, user=user, check_type=check_type, created_by=admin
                )
            else:
                raise CustomApiException(
                    "User is not registered for this event",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
        raise CustomApiException(
            "User record not found", status_code=status.HTTP_404_NOT_FOUND
        )

    @classmethod
    def get_checked_in_users(cls, event, created_by):
        return CheckIn.objects.filter(event=event, created_by=created_by)


class TicketService:
    @classmethod
    def create_ticket(cls, event, user, status, expiry_date):
        ticket_id = random_string(11)
        return Ticket.objects.create(
            event=event,
            owner=user,
            ticket_id=ticket_id.upper(),
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

    @classmethod
    def initiate_event_payment(cls, user, event_id, amount):
        from payment.service import PaymentManager

        event_amount = float(event.amount)
        if amount is None:
            raise CustomApiException(
                detail="This event is not free", status_code=status.HTTP_400_BAD_REQUEST
            )
        elif float(amount) < event_amount:
            raise CustomApiException(
                detail=f"Please input the proper amount - {event.currency}{event_amount}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Some financial calculations
        davent_deduction = 10  # TODO: come up with a formular to calculate this later
        amount_to_remit = float(amount) - davent_deduction

        # TODO: remit the davent_deduction into davent's Account, maybe in background

        # Initiate paystack payment

        initiate_payment, flag = PaymentManager.initiate_payment(
            user.email, amount_to_remit, event_id
        )
        return initiate_payment.get("response")

    @classmethod
    def verifiy_event_payment(cls, user, reference, event_id, payment_id, email):
        from payment.service import PaymentManager
        from event.tasks import generate_ticket_async

        verified_payment, flag = PaymentManager.verify_payment(
            reference, event_id, payment_id, email
        )

        if flag:
            event = cls.get_single_event(id=event_id)
            ticket = generate_ticket_async.delay(event, user, status, event.start_date)
            return verified_payment.get("response")
        else:
            return verified_payment
