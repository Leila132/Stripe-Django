from django.urls import path
from .views import BuyItemAPI, ItemAPI, OrderAPI, BuyOrderAPI, BuyItemAPI2, BuyOrderAPI2

urlpatterns = [
    #Stripe Session get id
    path('buy/<int:pk>', BuyItemAPI.as_view(), name='buy'),
    path('buy-order/<int:pk>', BuyOrderAPI.as_view(), name='buy-order'),
    #Stripe Payment Intent get id
    path('buy2/<int:pk>', BuyItemAPI2.as_view(), name='buy'),
    path('buy2-order/<int:pk>', BuyOrderAPI2.as_view(), name='buy-order'),
    #Buy
    path('item/<int:pk>', ItemAPI.as_view(), name='item'),
    path('order/<int:pk>', OrderAPI.as_view(), name='order'),
]