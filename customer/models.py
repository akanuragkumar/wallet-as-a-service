from django.db import models

from base.middleware.custom_manager import TenantAwareManager
from base.models import BaseModel
from tenant.models import Tenants


class Customer(BaseModel):
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE)  # Tenant identifier
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    # Use the tenant-aware manager
    objects = TenantAwareManager()

    def __str__(self):
        return f'{self.name} ({self.uuid})'

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
