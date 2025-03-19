from django.core.exceptions import BadRequest
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics

from interview.core.utils import is_valid_date
from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer


# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        start_date = query_params.get("start_date")
        embargo_date = query_params.get("embargo_date")
        q = Q()

        if start_date:
            if not is_valid_date(start_date):
                raise BadRequest("Invalid start_date format")
            q.add(Q(start_date__gte=start_date), Q.AND)
        if embargo_date:
            if not is_valid_date(embargo_date):
                raise BadRequest("Invalid embargo_date format")
            q.add(Q(embargo_date__lte=embargo_date), Q.AND)
        if q:
            return self.queryset.filter(q)
        return self.queryset.all()


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer
