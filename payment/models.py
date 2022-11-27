from django.db import models

from event.models import Event
from authentication.models import User
from helpers.db_helper import BaseAbstractModel


class Payment(BaseAbstractModel):
    STATUS = (("PENDING", "PENDING"), ("SUCCESS", "SUCCESS"), ("FAILED", "FAILED"))

    amount = models.DecimalField(
        max_digits=19,
        decimal_places=10,
    )
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payment_buyer"
    )
    status = models.CharField(max_length=30, choices=STATUS, default="PENDING")
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    payment_context = models.JSONField(default=dict, null=True, blank=True)
    transaction_context = models.JSONField(default=dict, null=True, blank=True)
    reference = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.buyer.first_name}'s for {self.event.name} "
