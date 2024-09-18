# ledger/serializers.py

from rest_framework import serializers
from .models import Ledger

class LedgerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ledger
        fields = ['transaction_type', 'amount', 'description']

class LedgerResponseSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Ledger
        fields = ['id', 'customer_name', 'transaction_type', 'amount', 'current_balance', 'description', 'created',
                  'modified']