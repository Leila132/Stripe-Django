import stripe
from .models import Item, Order, MONEY_C
import os

stripe.api_key = os.environ.get("stripe_api_key")

#Stripe Session
def make_session(obj, selected_currency):
    if isinstance(obj, Item):
        name = obj.name
        price = obj.price
    elif isinstance(obj, Order):
        name = f"Order #{obj.id}"
        price = obj.price
    else:
        raise TypeError(f"Unsupported object type: {type(obj)}")
    
    if obj.currency != selected_currency:
        if obj.currency == 'USD':
            price = price * MONEY_C
        else:
            price = price / MONEY_C
    price = round(price)
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': selected_currency.lower(),
                'product_data': {
                    'name': name,
                },
                'unit_amount': price*100, 
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost/success',
        cancel_url='http://localhost/cancel',
    )
    return {"id": session.id}
#Stripe PaymentIntent
def make_session2(obj, selected_currency):
    if isinstance(obj, Item):
        price = obj.price
    elif isinstance(obj, Order):
        price = obj.price
    else:
        raise TypeError(f"Unsupported object type: {type(obj)}")

    if obj.currency != selected_currency:
        if obj.currency == 'USD':
            price = price * MONEY_C
        else:
            price = price / MONEY_C
    price = round(price)
    intent = stripe.PaymentIntent.create(
        amount=price * 100, 
        currency=selected_currency.lower(),
        automatic_payment_methods={"enabled": True},
    )
    return {"id": intent.id, "client_secret": intent.client_secret}