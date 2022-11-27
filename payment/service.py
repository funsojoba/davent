import uuid
import requests
from django.conf import settings

from authentication.service import UserService

from payment.integrations.paystack import Paystack
from payment.models import Payment
from event.service import EventService

from payment.serializers import PaymentSerializer
from authentication.service import UserService


class PaymentManager:
    @classmethod
    def initiate_payment(cls, email, amount, event_id):
        event = EventService.get_single_event(id=event_id)
        buyer = UserService.get_user(email=email)

        # check existing payment for the same event by the same user
        payment = cls.get_single_payment(event=event, buyer=buyer, status="PENDING")
        if payment:
            return {
                "errors": "You have already initiated a payment for this event"
            }, False

        response = Paystack.initiate_payment(email, amount)
        if response:
            if response.get("status"):
                payment = Payment.objects.create(
                    reference=response.get("data").get("reference"),
                    amount=amount,
                    buyer=buyer,
                    event=event,
                )
                result = {
                    "response": response,
                    "payment": PaymentSerializer(payment).data,
                }
                return result, True
            else:
                return response, False
            return result, False
        return {
            "errors": "Could not initiate payment at this time, please try again later"
        }, False

    @classmethod
    def verify_payment(cls, reference, event_id, payment_id, email):
        event = EventService.get_single_event(id=event_id)
        buyer = UserService.get_user(email=email)

        response = Paystack.verify_payment(reference)
        if response:
            data = response["data"]

            if data["status"] == "success":
                payment = cls.get_single_payment(
                    id=payment_id, event=event, buyer=buyer, reference=reference
                )
                if payment:
                    payment.status = "SUCCESS"
                    payment_context = {
                        "reference": data["reference"],
                        "amount": data["amount"],
                        "id": data["id"],
                        "customer": data["customer"],
                        "transaction_date": data["transaction_date"],
                    }
                    payment.save()
                    return {"message": "Payment successful"}, True
                return {"errors": "Payment not found"}, False

            return {"errors": "Payment not successful"}, False
        print("RESPONSE:", response)
        return {
            "errors": "Could not initiate payment at this time, please try again later"
        }, False

    @classmethod
    def persist_payment_data(cls):
        pass

    @classmethod
    def get_payment_data(cls, payment_id, buyer_id):
        buyer = UserService.get_user(id=buyer_id)
        return Payment.objects.filter(id=payment_id, buyer=buyer).first()

    @classmethod
    def get_single_payment(cls, **kwargs):
        return Payment.objects.filter(**kwargs).first()

    @classmethod
    def list_payments(cls, **kwargs):
        if kwargs.get("buyer_id"):
            buyer = UserService.get_user(id=kwargs.get("buyer_id"))
            return Payment.objects.filter(buyer=buyer)

        if kwargs.get("event_id"):
            event = EventService.get_single_event(id=kwargs.get("event_id"))
            return Payment.objects.filter(event=event)

        return Payment.objects.filter(**kwargs)
