# serializers.py

from rest_framework import serializers

from ledger.models import Ledger
from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['transaction_id', 'customer', 'payment_gateway_reference',
                  'payment_gateway', 'amount', 'status', 'payment_date']

class LedgerSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)  # Link the payment if it exists

    class Meta:
        model = Ledger
        fields = ['customer', 'transaction_type', 'amount', 'current_balance',
                  'description', 'payment', 'created']
