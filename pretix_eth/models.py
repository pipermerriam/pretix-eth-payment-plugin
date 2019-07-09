from django.db import models
from django.core import validators

from pretix.base.models import Order


class CryptoPaymentRecord(models.Model):
    transaction_hash = models.BinaryField(
        max_length=32,
        validators=[
            validators.MaxLengthValidator(32),
            validators.MinLengthValidator(32),
        ]
    )
    chain_id = models.PositiveIntegerField()
    order_id = models.ForeignKey(Order, on_delete=models.PROTECT)

    class Meta:
        indexes = (
            models.Index(fields=('transaction_hash', 'chain_id')),
        )
        unique_together = (
            ('transaction_hash', 'chain_id'),
        )
