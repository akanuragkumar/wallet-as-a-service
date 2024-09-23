from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
HTTP_404_NOT_FOUND,
HTTP_200_OK
)

from base.authentication.tenant_authentication import APIKeySecretAuthentication
from base.middleware.CustomMetaDataMixin import CustomMetaDataMixin

from customer.models import Customer

from ledger.models import Ledger
from ledger.serializer import LedgerResponseSerializer


class LedgerView(CustomMetaDataMixin, APIView):
    authentication_classes = [APIKeySecretAuthentication]

    # GET: Get ledger history for a customer
    def get(self, request, customer_uuid):
        try:
            customer = Customer.objects.get(uuid=customer_uuid)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=HTTP_404_NOT_FOUND)

        ledger_entries = Ledger.objects.filter(customer=customer).order_by('-created')
        response_serializer = LedgerResponseSerializer(ledger_entries, many=True)
        return Response(response_serializer.data, status=HTTP_200_OK)
