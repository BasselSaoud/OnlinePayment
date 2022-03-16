# OnlinePayment
An extremely simple online payment API that mimics Paymob's (https://docs.paymob.com/docs/accept-standard-redirect), built with Django REST Framework

Usage:
1- Register a new user

URL: /register/
Method: POST

Example request:
{
  "username": "user",
  "password": "password"
}

Example response:
{
  "api_key": "ADsfnawAb4Dijds...."
}


2- Request an authentication token

URL: /auth/tokens/
Method: POST

Example request:
{
  "api_key": "ADsfnawAb4Dijds...."
}

Example response:
{
  "auth_token": "dnfBjdu485nDus...."
}


3- Register an order

URL: /orders/
Method: POST

Example request:
{
  "auth_token": "dnfBjdu485nDus....",
  "amount_cents": 100
}

Example response:
{
  "id": 1,
  "amount_cents": 100
}


4- Request payment token

URL: /payment/tokens/
Method: POST

Example request:
{
  "auth_token": "dnfBjdu485nDus....",
  "order_id": 1,
  "amount_cents": 100
}

Example response
{
  "payment_token": "kuqnIdbNq43Nd..."
}
