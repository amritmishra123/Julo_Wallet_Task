from  .tasks import update_wallet_balance
from django.contrib.auth.models import User
from .serializers import (
    WalletTransactionSerializer,
    WalletResponseSerializer)
from .models import Wallet, Account, Transaction
from rest_framework.authtoken.models import Token
from django.db import transaction


def build_response(status, data):
    response = {
        'status': status,
        'data': data}
    return response


def initialise_wallet(data):
    try:
        customer_xid = data.get('customer_xid')
        with transaction.atomic():
            existing_account = Account.objects.filter(customer_xid=customer_xid).last()
            if existing_account:
                user = existing_account.user
                if not existing_account.wallet:
                    Wallet.objects.create(account=existing_account)
            else:
                user = User.objects.create_user(username=customer_xid)
                account = Account.objects.create(customer_xid=customer_xid, user=user)
                Wallet.objects.create(account=account)
            token, created = Token.objects.get_or_create(user=user)
        return_data = {"token": token.key}
        response = build_response(status='success', data=return_data)
        return response
    except Exception as exc:
        return_data = {"error": str(exc)}
        response = build_response(status='failure', data=return_data)
        return response


def view_wallet(user, only_view=False):
    try:
        wallet = user.account.wallet
        status = 'success'
        if only_view and wallet.status:
            wallet_serializer = WalletResponseSerializer(wallet)
            return_data = {
                "wallet": wallet_serializer.data
            }
        elif not wallet.status and not only_view:
            wallet.status = True
            wallet.save()
            wallet_serializer = WalletResponseSerializer(wallet)
            return_data = {
                "wallet": wallet_serializer.data
            }
        elif wallet.status:
            return_data = {
                "error": "Already the wallet is enabled"
            }
            status = 'failure'
        else: 
            return_data = {
                "error": "Wallet is not enabled, please enable the wallet first to proceed further"
            }
            status = 'failure'

        response = build_response(status, return_data)
        return response
    except Exception as exc:
        return_data = {
                "error": str(exc)
            }
        response = build_response('failure', return_data)
        return response


def transaction_wallet(data, user, transaction_type):
    try:
        wallet = user.account.wallet
        if wallet.status:
            with transaction.atomic():
                serializer_class = WalletTransactionSerializer
                amount = data.get('amount')
                reference_id = data.get('reference_id')
                if transaction_type == 'withdrawl' and amount > wallet.balance:
                    return_data = {
                        "error": "Insufficient balance for the requested amount"}
                    return build_response('failure', return_data)
                update_wallet_balance. delay(int(amount), transaction_type, wallet.id)
                trx = Transaction.objects.create(
                    transaction_type=transaction_type,
                    transaction_by=wallet.account, amount=amount,
                    reference_id=reference_id)
            wallet_serializer = serializer_class(wallet, context={'trx': trx})
            return_data = {
                transaction_type: wallet_serializer.data
            }
            status = "success"
        else:
            return_data = {
                "error": 'Wallet is not enabled, please enable the wallet first to proceed further'
            }
            status = "failure"
        response = build_response(status, return_data)
        return response
    except Exception as exc:
        return_data = {"error": str(exc)}
        response = build_response('failure', return_data)
        return response


def disable_wallet(user):
    try:
        wallet = user.account.wallet
        if wallet.status:
            wallet.status = False
            wallet.save()
            serializer_wallet = WalletResponseSerializer(wallet, context={'disabled':True})
            status = 'success'
            return_data = {
                "wallet:": serializer_wallet.data
            }
        else:
            status = 'failure'
            return_data = {
                "error": "The wallet is already disabled"}
        response = build_response(status, return_data)
        return response
    except Exception as exc:
        return_data = {"errors:": str(exc)}
        response = build_response('failure', return_data)
        return response
