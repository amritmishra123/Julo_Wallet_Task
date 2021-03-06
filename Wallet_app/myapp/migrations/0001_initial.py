# Generated by Django 3.1.7 on 2022-03-15 05:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_xid', models.CharField(max_length=200, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=3, default=0, max_digits=20)),
                ('status', models.BooleanField(default=False)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.account')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('Deposit', 'deposit'), ('Withdraw', 'withdraw')], max_length=50)),
                ('amount', models.DecimalField(decimal_places=3, max_digits=20)),
                ('reference_id', models.CharField(max_length=200)),
                ('transaction_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.account')),
            ],
        ),
    ]
