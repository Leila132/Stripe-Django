from django.shortcuts import render
import stripe
from .models import Item, Order
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from .services import make_session, make_session2

class BaseBuyAPI(APIView):
    model = None
    def get_object(self, pk: int):
        return get_object_or_404(self.model, id=pk)
    
    def get(self, request: Request, pk: int) -> Response:
        obj = self.get_object(pk)
        selected_currency = request.query_params.get('currency', 'RUB')
        data = make_session(obj, selected_currency)
        return Response(data)

class BuyItemAPI(BaseBuyAPI):
    model = Item

class BuyOrderAPI(BaseBuyAPI):
    model = Order

class BaseObjectAPI(APIView):
    model = None
    name = ""
    def get_object(self, pk: int):
        return get_object_or_404(self.model, id=pk)
    def get(self, request: Request, pk:int) -> Response:
        obj = get_object_or_404(self.model, id=pk)
        return render(request, 'main/main.html', {'object': obj, 'type_of_obj': self.name})

class ItemAPI(BaseObjectAPI):
    model = Item
    name = "item"
    
class OrderAPI(BaseObjectAPI):
    model = Order
    name = "order"

#Для Stripe Payment Intent

class BaseBuyAPI2(APIView):
    model = None

    def get_object(self, pk: int):
        return get_object_or_404(self.model, id=pk)

    def get(self, request: Request, pk: int) -> Response:
        obj = self.get_object(pk)
        selected_currency = request.query_params.get('currency', 'RUB')
        data = make_session2(obj, selected_currency)
        return Response(data)

class BuyItemAPI2(BaseBuyAPI2):
    model = Item

class BuyOrderAPI2(BaseBuyAPI2):
    model = Order