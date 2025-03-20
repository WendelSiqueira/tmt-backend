from django.shortcuts import render
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer


# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrderTagGetCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer

    def get_filtered_queryset(self, pk: int):
        return self.queryset.filter(orders=pk)

    def get(self, request: Request, *args, **kwargs) -> Response:
        pk = kwargs["pk"]
        if pk is None:
            return Response({"error": "order pk is required"}, status=400)
        serializer = self.serializer_class(self.get_filtered_queryset(pk), many=True)

        return Response(serializer.data, status=200)
