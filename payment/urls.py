from django.urls import path

from payment.views import PaymentTransactionView

urlpatterns = [
    path('payment-transaction/', PaymentTransactionView.as_view(), name='payment-transaction'),
]