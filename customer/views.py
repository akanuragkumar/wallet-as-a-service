from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK

from base.authentication.tenant_authentication import APIKeySecretAuthentication
from base.middleware.CustomMetaDataMixin import CustomMetaDataMixin
from customer.models import Customer
from customer.serializers import CustomerUpdateSerializer, CustomerResponseSerializer, CustomerCreateSerializer


class CustomerView(CustomMetaDataMixin, APIView):
    # Apply authentication to all methods (tenant-aware via middleware)
    authentication_classes = [APIKeySecretAuthentication]

    def post(self, request):
        serializer = CustomerCreateSerializer(data=request.data)

        if serializer.is_valid():
            # Add tenant information to the serializer validated data
            validated_data = serializer.validated_data

            # Create the customer
            customer = Customer.objects.create(**validated_data)

            # Serialize the created customer for the response
            response_serializer = CustomerResponseSerializer(customer)
            return Response(response_serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # GET: Get customer details (must be part of tenant)
    def get(self, request, customer_uuid):
        try:
            customer = Customer.objects.get(uuid=customer_uuid)

            # Serialize the customer for the response
            response_serializer = CustomerResponseSerializer(customer)
            return Response(response_serializer.data, status=HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=HTTP_404_NOT_FOUND)

    def patch(self, request, customer_uuid):
        try:
            customer = Customer.objects.get(uuid=customer_uuid)

            # Deserialize request data
            serializer = CustomerUpdateSerializer(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                # Serialize and return the updated customer data
                response_serializer = CustomerResponseSerializer(customer)
                return Response(response_serializer.data, status=HTTP_200_OK)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
