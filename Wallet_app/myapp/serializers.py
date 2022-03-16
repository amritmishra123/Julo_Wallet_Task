from rest_framework import serializers
from .models import Wallet, Transaction
from datetime import datetime


class InitSerializer(serializers.Serializer):
    customer_xid = serializers.CharField()


class TransactionRequestSerializer(serializers.ModelSerializer):

    def validate_reference_id(self, value):
        trx_type = self.context.get('trx_type')
        account = self.context.get('account')
        if Transaction.objects.filter(reference_id=value, transaction_type=trx_type, transaction_by=account).exists():
            raise serializers.ValidationError("'reference_id': '{}' for trx '{}' is already used".format(value, trx_type))
        else:
            return value

    class Meta:
        model = Transaction
        fields = ('amount', 'reference_id')

class DisableWalletRequestSerializer(serializers.Serializer):
    is_disabled = serializers.BooleanField()

    def validate_is_disabled(self, value):
        if value is True:
            return value
        else:
            raise serializers.ValidationError("'is_disabled' must be True to disable the wallet" )

class WalletResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    owned_by = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    enabled_at = serializers.SerializerMethodField()

    def get_owned_by(self, instance):
        return instance.account.customer_xid

    def get_status(self, instance):
        if instance.status:
            return 'enabled'
        else:
            return 'disabled'

    def get_enabled_at(self, instance):
        now = datetime.now()
        return str(now)

    def to_representation(self, instance):
        data = super(WalletResponseSerializer, self). \
            to_representation(instance)
        disabled = self.context.get('disabled')
        if disabled:
            data['disabled_at'] = data['enabled_at']
            data.pop('enabled_at')
        return data

    class Meta:
        model = Wallet
        fields = ('id', 'owned_by', 'status', 'enabled_at', 'balance')


class WalletTransactionSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    transaction_by = serializers.CharField(source='account_id')
    transaction_at = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    reference_id = serializers.SerializerMethodField()

    def get_transaction_at(self, instance):
        now = datetime.now()
        return str(now)

    def get_amount(self, instance):
        last_trx = self.context.get('trx')
        return str(last_trx.amount)
    
    def get_reference_id(self, instance):
        last_trx = self.context.get('trx')
        return last_trx.reference_id

    def to_representation(self, instance):
        data = super(WalletTransactionSerializer, self). \
            to_representation(instance)
        data['status'] = 'success'
        last_trx = self.context.get('trx')
        if last_trx.transaction_type == 'deposit':
            data['deposited_by'] = data['transaction_by']
            data['deposited_at'] = data['transaction_at']
        elif last_trx.transaction_type == 'withdrawl':
            data['withdrawn_by'] = data['transaction_by']
            data['withdrawn_at'] = data['transaction_at']
        data.pop('transaction_by')
        data.pop('transaction_at')
        return data

    class Meta:
        model = Wallet
        fields = ('id', 'transaction_by', 'transaction_at', 'amount', 'reference_id')
