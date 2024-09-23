from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from customer.models import Customer
from ledger.choices import TransactionTypesChoices
from ledger.models import Ledger
from payment.models import Payment
from payment.serializer import LedgerSerializer, PaymentSerializer


class PaymentTransactionView(APIView):

    @transaction.atomic
    def post(self, request):
        data = request.data
        customer_id = data.get('customer_id')
        transaction_type = data.get('transaction_type')  # credit or debit
        amount = data.get('amount')
        payment_gateway_reference = data.get('payment_gateway_reference', None)
        payment_gateway = data.get('payment_gateway', 'cashfree')  # default if not provided
        description = data.get('description', '')

        try:
            # Fetch the customer
            customer = Customer.objects.get(id=customer_id)

            # Credit transaction (Adding money)
            if transaction_type == 'credit':
                # Create a payment entry
                payment = Payment.objects.create(
                    customer=customer,
                    payment_gateway_reference=payment_gateway_reference,
                    payment_gateway=payment_gateway,
                    amount=amount,
                    status='completed'  # Assuming payment succeeds
                )

                # Create a ledger entry for the credit
                ledger_entry = Ledger.objects.create(
                    customer=customer,
                    payment=payment,
                    transaction_type=TransactionTypesChoices.CREDIT,
                    amount=amount,
                    current_balance=customer.calculated_balance() + amount,  # Calculate new balance
                    description=description
                )
                message = 'Money credited to wallet successfully.'

            # Debit transaction (Spending money)
            elif transaction_type == 'debit':
                if customer.balance < amount:
                    return Response({'error': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)

                # Create a ledger entry for the debit
                ledger_entry = Ledger.objects.create(
                    customer=customer,
                    payment=None,  # No payment linked for debit transactions
                    transaction_type=TransactionTypesChoices.DEBIT,
                    amount=amount,
                    current_balance=customer.calculated_balance() - amount,  # Calculate new balance
                    description=description
                )
                message = 'Money debited from wallet successfully.'

            # Return response
            return Response({
                'status': 'success',
                'message': message,
                'ledger': LedgerSerializer(ledger_entry).data,
                'payment': PaymentSerializer(payment).data if transaction_type == 'credit' else None
            }, status=status.HTTP_201_CREATED)

        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
