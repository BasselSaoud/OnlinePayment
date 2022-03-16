from django.db import models

# Simple User Model
class SimpleUser(models.Model):
    username = models.CharField(primary_key=True, max_length=100)
    password = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add = True)

# API Key model
class APIKey(models.Model):
    api_key = models.CharField(primary_key=True, max_length=64)
    user = models.ForeignKey(
        'SimpleUser',
        on_delete = models.CASCADE,
    )

# Authentication Token model
class AuthenticationToken(models.Model):
    auth_token = models.CharField(primary_key=True, max_length=64)
    api_key = models.ForeignKey(
        'APIKey',
        on_delete = models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add = True)

# Order model
class Order(models.Model):
    amount_cents = models.BigIntegerField()

# Payment Token model
class PaymentToken(models.Model):
    payment_token = models.CharField(primary_key=True, max_length=64)
    order = models.ForeignKey(
        'Order',
        on_delete = models.CASCADE,
    )
    amount_cents = models.BigIntegerField()