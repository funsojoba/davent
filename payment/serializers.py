from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Payment
        fields = ["id","amount", "amount", "buyer","status", "event"]


class InitiatePaymentSerializer(serializers.Serializer):
    event_id = serializers.CharField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
    
class VerifyPaymentSerializer(serializers.Serializer):
    event_id = serializers.CharField()
    payment_id = serializers.CharField()
    reference = serializers.CharField()
    
    