#Import our models and Django REST Framework serializers
from Pay.models import SimpleUser, APIKey, AuthenticationToken
from rest_framework import serializers

#SimpleUser model serializer
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleUser
        fields = '__all__'

#APIKey model serializer
class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ['api_key']

#Payment token serializer
class AuthenticationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationToken
        fields = ['token']