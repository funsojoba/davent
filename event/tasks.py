from celery import shared_task
from django.utils import timezone
from decouple import config

from datetime import timedelta

from event.service import EventService
from authentication.service import UserService

from notification.service import EmailService


@shared_task()
def generate_ticket_async(event_id, user_id, status, expiry_date):
    from event.service import TicketService

    event = EventService.get_single_event(id=event_id)
    user = UserService.get_user(id=user_id)

    TicketService.create_ticket(event, user, status, expiry_date)

    # TODO: Generate PDF, upload to AWS or Cloudinary and send email with link to user


@shared_task(name="task.update-old-event-status")
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


@shared_task(name="task.remind-user-of-event")
def user_event_reminder():
    """
    This task method is meant to alert users of the event they registered for
    """
    days = {"1": "tomorrow", "7": "next week"}

    events = EventService.get_events()  # get active events
    for event in events:
        event_start_date = event.start_date

        today = timezone.now()

        # if difference == 7, date = days.get(7)
        # if difference = 1, date = days.get(1)
        # for participant in event.event_participant:
        # send email

        # Get the amount of days left
        day_diff = event.start_date.day - today.day

        # only dealing with a day and a week
        if day_diff in [1, 7]:
            event_day = days.get(str(day_diff))
            # only send the email in a day or a week
            for participant in event.participant.all():
                context = {
                    "event_name": event.name,
                    "first_name": participant.first_name,
                    "event_day": event_day,
                    "event_date": event.start_date,
                    "event_location": event.location,
                    "event_type": event.event_type,
                    "event_url": event.event_url if event.event_url else None,
                    "event_address": event.address if event.address else None,
                    "rsvp": ", ".join(event.rsvp) if event.rsvp else None,
                }

                # TODO: only send email to verified email,
                EmailService.send_async(
                    "user_event_reminder.html",
                    "Event Registration",
                    [participant.email],
                    context=context,
                )


def test_email_reminder(event_id):
    days = {"1": "tomorrow", "7": "next week"}
    event = EventService.get_single_event(id=event_id)
    today = timezone.now()
    day_diff = event.start_date.day - today.day

    event_day = days.get(str(day_diff))
    for participant in event.participant.all():
        context = {
            "event_name": event.name,
            "first_name": participant.first_name,
            "event_day": event_day,
            "event_date": event.start_date,
            "event_location": event.location,
            "event_type": event.event_type,
            "event_url": f"{config('BASE_URL')}/event/{event.id}",
            "event_address": event.address if event.address else None,
            "rsvp": ", ".join(event.rsvp) if event.rsvp else None,
        }

        # TODO: only send email to verified email,
        EmailService.send_async(
            "user_event_reminder.html",
            "Event Registration",
            [participant.email],
            context=context,
        )
