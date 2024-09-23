import uuid

from django.db import models
from django.db.transaction import atomic
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by

from customer.models import Customer
from payment.choices import PaymentStatusChoices, PaymentGatewayChoices


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    payment_gateway_reference = models.CharField(max_length=255, blank=True, null=True)  # Gateway reference
    payment_gateway = models.CharField(max_length=50, choices=PaymentGatewayChoices,
                                       default=PaymentGatewayChoices.CASHFREE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=PaymentStatusChoices,
                                       default=PaymentStatusChoices.INITIATED)
    payment_date = models.DateTimeField(auto_now_add=True)

    @atomic
    @fsm_log_by
    @transition(field='status', source=[PaymentStatusChoices.INITIATED],
                target=PaymentStatusChoices.SUCCESS, conditions=[])
    def mark_status_success(self, by=None):
        pass

    @atomic
    @fsm_log_by
    @transition(field='status', source=[PaymentStatusChoices.INITIATED],
                target=PaymentStatusChoices.FAILED, conditions=[])
    def mark_status_failed(self, by=None):
        pass

    @atomic
    @fsm_log_by
    @transition(field='status', source=[PaymentStatusChoices.FAILED],
                target=PaymentStatusChoices.SUCCESS, conditions=[])
    def mark_status_failed_to_success(self, by=None):
        pass

    @atomic
    @fsm_log_by
    @transition(field='status', source=[PaymentStatusChoices.INITIATED],
                target=PaymentStatusChoices.CANCELLED, conditions=[])
    def mark_status_initiated_to_cancelled(self, by=None):
        pass

    @atomic
    @fsm_log_by
    @transition(field='status', source=[PaymentStatusChoices.FAILED],
                target=PaymentStatusChoices.CANCELLED, conditions=[])
    def mark_status_failed_to_cancelled(self, by=None):
        pass

    @atomic
    @fsm_log_by
    @transition(field='status', source=[PaymentStatusChoices.SUCCESS],
                target=PaymentStatusChoices.REFUND_INITIATED, conditions=[])
    def mark_status_success_to_refund_initiated(self, by=None):
        pass

    @atomic
    @fsm_log_by
    @transition(field='status', source=[PaymentStatusChoices.SUCCESS],
                target=PaymentStatusChoices.REFUNDED, conditions=[])
    def mark_status_success_to_refunded(self, by=None):
        pass

    @atomic
    @fsm_log_by
    @transition(field='status', source=[PaymentStatusChoices.REFUND_INITIATED],
                target=PaymentStatusChoices.REFUNDED, conditions=[])
    def mark_status_refund_initiated_to_refunded(self, by=None):
        pass

    def __str__(self):
        """Represent PaymentTransactions object as string."""
        return '{} {} {}'.format(self.amount, self.status, self.customer.name)

class Cashfree(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='cashfree')
    order_id = models.CharField(
        max_length=200, null=True, blank=True, db_index=True)
    currency = models.CharField(max_length=100,
                                choices=PaymentGatewayChoices,
                                default=PaymentGatewayChoices.CASHFREE)
    notes = models.JSONField(default=dict, null=True, blank=True)
    redirect_url = models.CharField(max_length=200, null=True, blank=True)
    cf_refund_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.order_id}'
