from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    customer_xid = models.CharField(max_length=200, unique=True) # Can be used as FK to an existing customer model
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)


class Wallet(models.Model):
    account = models.OneToOneField(Account, on_delete=models.DO_NOTHING)
    balance = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    status = models.BooleanField(default=False)


class Transaction(models.Model):
    TRANSACTION_CHOICES = (
        ('Deposit', 'deposit'),
        ('Withdraw', 'withdraw')
    )
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_CHOICES)
    transaction_by = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=20, decimal_places=3)
    reference_id = models.CharField(max_length=200)

