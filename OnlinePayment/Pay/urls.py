from django.urls import path
from Pay.views import RegisterSimpleUser, GetAuthenticationToken

urlpatterns = [
    path('register/', RegisterSimpleUser),
    path('auth/tokens/', GetAuthenticationToken)
]