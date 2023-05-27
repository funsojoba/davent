from celery import shared_task
from django.utils import timezone

from event.service import EventService
from authentication.service import UserService


@shared_task()
def generate_ticket_async(event_id, user_id, status, expiry_date):
    from event.service import TicketService

    event = EventService.get_single_event(id=event_id)
    user = UserService.get_user(id=user_id)

    TicketService.create_ticket(event, user, status, expiry_date)


@shared_task(name="update-old-event-status")
def update_old_event_status():
    """
    This task method looks through the database for events that are expired and update their status accordingly
    """
    today = timezone.now()
    old_events = EventService.get_events(end_date__lte=today)
    if old_events:
        for event in old_events:
            event.status = "EXPIRED"
            event.save()
