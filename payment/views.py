from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

# from helpers.permissions import IsAdminUser, IsUser
from helpers.response import Response

from .serializers import (
    InitiatePaymentSerializer,
    VerifyPaymentSerializer,
    PaymentSerializer,
)

from payment.service import PaymentManager
from helpers.permissions import IsAdminUser, IsUser


class PaymentViewset(viewsets.ViewSet):
    @action(methods=["POST"], detail=False, url_path="initiate")
    def initiate_payment(self, request):
        serializer = InitiatePaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors=serializer.errors)

        service_response = PaymentManager.initiate_payment(
            email=request.user.email,
            amount=serializer.data["amount"],
            event_id=serializer.data["event_id"],
        )
        response, flag = service_response
        if flag:
            return Response(data=response)
        return Response(errors=response, status=400)

    @action(methods=["POST"], detail=False, url_path="verify")
    def verify_payment(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors=serializer.errors)

        service_response, flag = PaymentManager.verify_payment(
            reference=serializer.data["reference"],
            event_id=serializer.data["event_id"],
            payment_id=serializer.data["payment_id"],
            email=request.user.email,
        )
        if flag:
            return Response(data=service_response)
        return Response(errors=service_response, status=400)


class AdminPaymentViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    def list(self, request):
        response = PaymentManager.list_payments(**request.GET.dict())
        serializer = PaymentSerializer(response, many=True)
        return Response(data={"payments": serializer.data})
