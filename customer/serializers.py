from rest_framework import serializers
from customer.models import Customer

class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'email', 'balance']
        extra_kwargs = {
            'name': {'required': False},
            'phone_number': {'required': False},
            'email': {'required': False},
            'balance': {'required': False}
        }


class CustomerResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['uuid', 'name', 'phone_number', 'email', 'balance', 'created', 'modified']


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'email', 'balance']


class CustomerResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['uuid', 'name', 'phone_number', 'email', 'balance', 'created', 'modified']
