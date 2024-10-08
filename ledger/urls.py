# ledger/urls.py

from django.urls import path

from ledger.views import LedgerView

urlpatterns = [
    path('<uuid:customer_uuid>/', LedgerView.as_view(), name='customer-ledger'),
]