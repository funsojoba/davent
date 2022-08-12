from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

# from helpers.permissions import IsAdminUser, IsUser
from helpers.response import Response

from .serializers import InitiatePaymentSerializer, VerifyPaymentSerializer

from payment.service import PaymentManager


class PaymentViewset(viewsets.ViewSet):
    
    
    @action(methods=["POST"], detail=False, url_path="initiate")
    def initiate_payment(self, request):
        serializer = InitiatePaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors=serializer.errors)
        
        service_response = PaymentManager.initiate_payment(
            email=request.user.email, 
            amount=serializer.data['amount'], 
            event_id=serializer.data["event_id"])
        return Response(data=service_response)
    
    @action(methods=["POST"], detail=False, url_path="verify")
    def verify_payment(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors=serializer.errors)
        
        service_response = PaymentManager.verify_payment(
            reference=serializer.data['reference'], 
            amount=serializer.data['amount'], 
            payment_id=serializer.data["payment_id"])
        return Response(data=service_response)
        
        