import uuid
import requests
from django.conf import settings


class Paystack:
    
    BASE_URL = settings.PAYSTACK_URL
    
    @classmethod
    def generate_reference(cls, prefix=""):
        import uuid

        return f"{prefix}-{uuid.uuid4().hex}"
    
    
    @classmethod
    def _initiate_request(cls, endpoint, payload, method="POST"):
        url = f"{BASE_URL}{endpoint}"
        
        headers = {
            "Accept":"application/json",
            "Authorization": f"Bearer {setting.PAYSTACK_SECRET_KEY}",
        }
        if method == "GET":
            response = requests.request(method, url, headers=headers)
        else:
            response = requests.request(method, url, headers=headers, json=payload)
        return response.json()
    
    
    @classmethod
    def initiate_payment(cls, email, amount):
        payload = {
            "email":email,
            "amount":amount,
            "reference": cls.generate_reference("EV")
        }
        try:
            cls._initiate_request(endpoint, payload)
        except:
            return False