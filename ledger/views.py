from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (HTTP_400_BAD_REQUEST,
                                   HTTP_201_CREATED,
                                   HTTP_404_NOT_FOUND,
                                   HTTP_200_OK)

from base.authentication.tenant_authentication import APIKeySecretAuthentication
from base.middleware.CustomMetaDataMixin import CustomMetaDataMixin

from customer.models import Customer

from ledger.models import Ledger
from ledger.serializer import LedgerRequestSerializer, LedgerResponseSerializer


class LedgerView(CustomMetaDataMixin, APIView):
    authentication_classes = [APIKeySecretAuthentication]

    # POST: Create a new ledger entry for a customer
    def post(self, request, customer_uuid):
        try:
            customer = Customer.objects.get(uuid=customer_uuid)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=HTTP_404_NOT_FOUND)

        serializer = LedgerRequestSerializer(data=request.data)
        if serializer.is_valid():
            ledger_entry = serializer.save(customer=customer)
            response_serializer = LedgerResponseSerializer(ledger_entry)
            return Response(response_serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # GET: Get ledger history for a customer
    def get(self, request, customer_uuid):
        try:
            customer = Customer.objects.get(uuid=customer_uuid)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=HTTP_404_NOT_FOUND)

        ledger_entries = Ledger.objects.filter(customer=customer).order_by('-created')
        response_serializer = LedgerResponseSerializer(ledger_entries, many=True)
        return Response(response_serializer.data, status=HTTP_200_OK)
