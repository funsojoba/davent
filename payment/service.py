import uuid
import requests
from django.conf import settings

from authentication.service import UserService

from payment.integrations.paystack import Pay

class PaymentManager:
    

    @classmethod
    def make_payment(cls):
        pass

    @classmethod
    def persist_payment_data(cls):
        pass

    @classmethod
    def get_payment_data(cls, payment_id, buyer_id):
        buyer = UserService.get_user(id=buyer_id)
        return Payment.objects.filter(id=payment_id, buyer=buyer).first()
