import uuid
import requests

from authentication.service import UserService


class PaymentManager:
    
    @classmethod
    def generate_reference(cls):
        pass
    
    @classmethod
    def _initiate_request(cls):
        pass

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
