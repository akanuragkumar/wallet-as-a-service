from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


from base.authentication.tenant_authentication import APIKeySecretAuthentication
from base.middleware.CustomMetaDataMixin import CustomMetaDataMixin

from customer.models import Customer

from ledger.models import Ledger
from ledger.serializer import LedgerResponseSerializer


# Custom pagination class
class LedgerPagination(PageNumberPagination):
    page_size = 10  # Number of ledger entries per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class LedgerView(CustomMetaDataMixin, ListAPIView):
    authentication_classes = [APIKeySecretAuthentication]
    serializer_class = LedgerResponseSerializer
    pagination_class = LedgerPagination

    def get_queryset(self):
        customer_uuid = self.kwargs['customer_uuid']
        try:
            customer = Customer.objects.get(uuid=customer_uuid)
        except Customer.DoesNotExist:
            raise NotFound(detail="Customer not found")
        return Ledger.objects.filter(customer=customer).order_by('-created')

    # GET: Get ledger history for a customer with pagination
    def list(self, request, customer_uuid):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            response_serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(response_serializer.data)

        response_serializer = self.get_serializer(queryset, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
