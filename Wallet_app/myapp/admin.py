from django.contrib import admin

from .models import Account,Wallet,Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['customer_xid','user']
    
    
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['account','balance','status']
    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['TRANSACTION_CHOICES','transaction_type','transaction_by','amount','reference_id'] 
