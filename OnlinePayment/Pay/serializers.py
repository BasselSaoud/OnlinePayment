#Import our models and Django REST Framework serializers
from ast import Or
from Pay.models import *
from rest_framework import serializers

# SimpleUser model serializer
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleUser
        fields = '__all__'

# APIKey model serializer
class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ['api_key']

# Authentication token serializer
class AuthenticationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationToken
        fields = ['auth_token']

# Order serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'amount_cents']

# Payment token serializer
class PaymentTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentToken
        fields = ['payment_token']