from math import e

from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer


# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class DeactivateOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request: Request, *args, **kwargs) -> Response:
        state = kwargs.get("state")
        pk = kwargs.get("pk")
        print(state, pk)
        if not pk or not isinstance(pk, int):
            return Response({"error": "Order ID is required"}, status=400)
        if state == "activate":
            print("activate")
            Order.activate(pk)
        elif state == "deactivate":
            Order.deactivate(pk)

        order = self.get_object()
        serializer = self.get_serializer(order)

        return Response(serializer.data)
