import uuid
import requests
from django.conf import settings

from authentication.service import UserService

from payment.integrations.paystack import Paystack
from payment.models import Payment
from event.service import EventService

class PaymentManager:
    
    @classmethod
    def initiate_payment(cls, email, amount, event_id):
        event = EventService.get_single_event(id=event_id)
        buyer = UserService.get_user(email=email)
        response = Paystack.initiate_payment(email, amount)
        if response:
            payment = Payment.objects.create(
                amount=amount,
                buyer=buyer,
                status="PENDING",
                event=event,
                payment_context=response
            )
            return response, payment
        return {"errors":"Could not initiate payment at this time, please try again later"}

    @classmethod
    def verify_payment(cls, reference, event, payment_id):
        pass
    
    @classmethod
    def persist_payment_data(cls):
        pass

    @classmethod
    def get_payment_data(cls, payment_id, buyer_id):
        buyer = UserService.get_user(id=buyer_id)
        return Payment.objects.filter(id=payment_id, buyer=buyer).first()
