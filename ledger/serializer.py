# ledger/serializers.py

from rest_framework import serializers
from ledger.models import Ledger

class LedgerResponseSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    transaction_id = serializers.CharField(source='payment.transaction_id', read_only=True)

    class Meta:
        model = Ledger
        fields = ['id', 'customer_name', 'transaction_id','transaction_type',
                  'amount', 'current_balance', 'description', 'created',
                  'modified']
