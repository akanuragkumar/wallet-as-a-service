from django.urls import path
from .views import CustomerView

urlpatterns = [
    path('', CustomerView.as_view(), name='create-customer'),  # POST for customer creation
    path('<str:customer_uuid>/', CustomerView.as_view(), name='customer-details'),  # GET and PUT for customer
]