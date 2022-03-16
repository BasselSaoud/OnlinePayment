from os import stat
from datetime import *
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Pay.models import *
from Pay.serializers import *
from passlib.hash import pbkdf2_sha256
import pytz

# Register simple user
@api_view(['POST'])
def registerSimpleUser(request):
    serializer = SimpleUserSerializer(data=request.data)

    # Valid user input, start registration
    if serializer.is_valid():

        # Check if user already registered
        user = SimpleUser.objects.filter(username=request.data['username'])
        if user.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Register user
        serializer.save()

        # Get user model instance
        user = SimpleUser.objects.get(username=request.data['username'])
        # Generate API Key for user
        generated_key = pbkdf2_sha256.hash(user.username + user.date_created.strftime('%c')) #datetime.now().strftime('%c')

        # Create a new API Key for the user and save it to the database
        api_key = APIKey.objects.create(api_key=generated_key, user=user)
        api_key.save()

        # Serialize and respond
        api_keySerializer = APIKeySerializer(instance=api_key)
        return Response(api_keySerializer.data, status=status.HTTP_201_CREATED)

    # Invalid user input
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get authentication token
@api_view(['POST'])
def getAuthenticationToken(request):
    
    # If request data has no api key respond with 400 bad request
    try:
        api_key = request.data['api_key']
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Check if API Key is valid
    api_key = APIKey.objects.filter(api_key=request.data['api_key'])
    if not api_key.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Check if a authentication token exists 
    authentication_token = AuthenticationToken.objects.filter(api_key=request.data['api_key'])
    if authentication_token.exists():
        
        # If it exists and has not expired respond
        authentication_token = AuthenticationToken.objects.get(api_key=request.data['api_key'])
        if abs(datetime.now(pytz.utc) - authentication_token.date_created).total_seconds() < 3600:
            return Response(AuthenticationTokenSerializer(instance=authentication_token).data, status=status.HTTP_200_OK)

    # Get api key instance
    api_key = APIKey.objects.get(api_key=request.data['api_key'])

    # Create authentication token
    token = pbkdf2_sha256.hash(api_key.api_key + datetime.now().strftime('%c'))
    authentication_token = AuthenticationToken.objects.create(token=token, api_key=api_key)
    authentication_token.save()

    # Serialize and respond
    authentication_tokenSerializer = AuthenticationTokenSerializer(instance=authentication_token)
    return Response(authentication_tokenSerializer.data, status=status.HTTP_201_CREATED)

# Register new order
@api_view(['POST'])
def registerOrder(request):
    
    # If request data has no api key respond with 400 bad request
    try:
        auth_token = request.data['auth_token']
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Check authentication token validity
    auth_token = AuthenticationToken.objects.filter(token=request.data['auth_token'])
    if not auth_token.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Check if authentication token expired
    date_created = AuthenticationToken.objects.get(token=request.data['auth_token']).date_created
    if abs(datetime.now(pytz.utc) - date_created).total_seconds() > 3600:
        return Response({"error": "authentication token has expired"}, status=status.HTTP_403_FORBIDDEN)

    # Create order
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # Incorrect input
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get payment token
@api_view(['POST'])
def getPaymentToken(request):
    
    # If request data has no api key respond with 400 bad request
    try:
        auth_token = request.data['auth_token']
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Check authentication token validity
    auth_token = AuthenticationToken.objects.filter(token=request.data['auth_token'])
    if not auth_token.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Check if authentication token expired
    date_created = AuthenticationToken.objects.get(token=request.data['auth_token']).date_created
    if abs(datetime.now(pytz.utc) - date_created).total_seconds() > 3600:
        return Response({"error": "authentication token has expired"}, status=status.HTTP_403_FORBIDDEN)

    # Check if order exists
    order = Order.objects.filter(id=request.data['order_id'])
    if not order.exists():
        return Response({'error': 'order not found'}, status=status.HTTP_404_NOT_FOUND)

    # Get order and create new payment
    order = Order.objects.get(id=request.data['order_id'])
    token = pbkdf2_sha256.hash(order.id + datetime.now().strftime('%c'))
    payment_token = PaymentToken.objects.create(payment_token=token, order=order)
    serializer = PaymentTokenSerializer(instance=payment_token)
    serializer.save()
    return Response(data=serializer, status=status.HTTP_201_CREATED)