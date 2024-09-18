from django.db import models
from base.models import BaseModel
from customer.models import Customer
from ledger.choices import TRANSACTION_TYPES


class Ledger(BaseModel):
    customer = models.ForeignKey(Customer, related_name='ledger_entries', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=(('credit', 'Credit'), ('debit', 'Debit')))
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_balance = models.DecimalField(max_digits=10,
                                          decimal_places=2)  # Store customer's balance at the time of this transaction
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculate current balance when creating the ledger entry
        if not self.pk:  # Only on creation
            if self.transaction_type == 'credit':
                self.current_balance = self.customer.calculated_balance() + self.amount
            else:
                self.current_balance = self.customer.calculated_balance() - self.amount

        super().save(*args, **kwargs)

        # Update customer's cached balance after the ledger entry
        self.customer.balance = self.customer.calculated_balance()
        self.customer.save()

    def __str__(self):
        return f'Ledger Entry for {self.customer.name}: {self.transaction_type} of {self.amount}'

    class Meta:
        verbose_name = 'Ledger'
        verbose_name_plural = 'Ledgers'
        ordering = ['-created']
