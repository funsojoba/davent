from django.db import models
from helpers.db_helper import BaseAbstractModel


class EventCategory(BaseAbstractModel):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey("authentication.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Event Category"
        verbose_name_plural = "Event Categories"


class Event(BaseAbstractModel):
    STATUS = (("ACTIVE", "ACTIVE"), ("EXPIRED", "EXPIRED"))
    TYPE = (("FREE", "FREE"), ("PAID", "PAID"))

    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    owner = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    participant = models.ManyToManyField(
        "authentication.User",
        related_name="participant",
        verbose_name="event participants",
    )
    status = models.CharField(max_length=50, choices=STATUS)
    event_type = models.CharField(max_length=50, choices=TYPE)
    category = models.ForeignKey(EventCategory, on_delete=models.DO_NOTHING)
    event_banner = models.URLField(blank=True, null=True)
    event_dp = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
