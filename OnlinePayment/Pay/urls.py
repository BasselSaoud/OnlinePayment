from django.urls import path
from Pay.views import *

urlpatterns = [
    path('register/', registerSimpleUser),
    path('auth/tokens/', getAuthenticationToken),
    path('orders/', registerOrder),
    path('payment/tokens/', getPaymentToken)
]