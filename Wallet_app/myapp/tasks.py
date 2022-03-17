from .models import  Wallet
from celery import shared_task


@shared_task
def update_wallet_balance(amount, trx_type, wallet_id):
    wallet = Wallet.objects.get(id=wallet_id)
    if trx_type == 'deposit':
        wallet.balance = wallet.balance + int(amount)
    else:
        wallet.balance = wallet.balance - int(amount)
    wallet.save()
   
