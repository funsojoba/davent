import string
import random

from django.db import models
from django.utils import timezone

from helpers.db_helper import BaseAbstractModel
from organization.models import Organization

# from django_location_field.models import LocationField


def get_ticket_id():
    string_chr = string.ascii_uppercase + string.digits
    return "".join(random.choices(string_chr, k=8))


def get_currency():
    # TODO: update this to a list of currencies ISO
    return "NGN"


class EventCategory(BaseAbstractModel):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey("authentication.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Event Category"
        verbose_name_plural = "Event Categories"


class Event(BaseAbstractModel):
    STATUS = (("ACTIVE", "ACTIVE"), ("EXPIRED", "EXPIRED"), ("SCHEDULED", "SCHEDULED"))
    TYPE = (("FREE", "FREE"), ("PAID", "PAID"))
    LOCATION = (("ONLINE", "ONLINE"), ("ONSITE", "ONSITE"))

    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    owner = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    participant = models.ManyToManyField(
        "authentication.User",
        related_name="participant",
        verbose_name="event participants",
        blank=True,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="organization",
        verbose_name="event organization",
    )
    status = models.CharField(max_length=50, choices=STATUS)
    event_type = models.CharField(max_length=50, choices=TYPE)
    category = models.ForeignKey(EventCategory, on_delete=models.DO_NOTHING)
    event_banner = models.URLField(blank=True, null=True)
    event_dp = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=50, choices=LOCATION)
    event_city = models.CharField(max_length=256, null=True)
    event_state = models.CharField(max_length=200, null=True, blank=True)
    event_country = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)
    currency = models.CharField(max_length=5, default=get_currency)
    event_url = models.URLField(blank=True, null=True)
    rsvp = models.JSONField(default=list, null=True, blank=True)
    participant_capacity = models.IntegerField(
        default=0, verbose_name="How many people can register"
    )
    remaining_slots = models.IntegerField(default=0)
    # event_location = LocationField(blank=True, null=True)
    def __str__(self):
        return self.name

    @property
    def get_participant_count(self):
        return self.participant.count()

    @property
    def get_status(self):
        status = ""
        if timezone.now() > self.end_date:
            status = self.STATUS[1][0]
        else:
            status = self.STATUS[0][0]
        return status


class Ticket(BaseAbstractModel):
    STATUS = (("ACTIVE", "ACTIVE"), ("EXPIRED", "EXPIRED"), ("INVALID", "INVALID"))
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket")
    owner = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    ticket_id = models.CharField(max_length=256, default=get_ticket_id)
    status = models.CharField(choices=STATUS, max_length=20)
    expiry_date = models.DateTimeField()

    @property
    def get_status(self):
        today = timezone.now()
        event_end_date = self.event.end_date

        if today > event_end_date:
            return self.STATUS[1][0]
        else:
            return self.STATUS[0][0]


class CheckIn(BaseAbstractModel):
    TYPE = (("CHECK_IN", "CHECK_IN"), ("CHECK_OUT", "CHECK_OUT"))
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey("authentication.User", on_delete=models.DO_NOTHING)
    check_type = models.CharField(max_length=50, choices=TYPE, default=TYPE[0][0])


class EventPayment(BaseAbstractModel):
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE)
    payment = models.ForeignKey("payment.Payment", on_delete=models.CASCADE)
    ticket = models.ForeignKey("event.Ticket", on_delete=models.CASCADE)

    """
        >>> Create event
        >>> if event is paid, create payment and ticket
        >>> then create event payment (EventPayment model) to link event and payment
    """
