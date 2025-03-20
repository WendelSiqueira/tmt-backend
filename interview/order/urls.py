
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, OrderOnTagGetCreateView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('tags/<int:pk>/orders', OrderOnTagGetCreateView.as_view(), name='tag-order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),

]