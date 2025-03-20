
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, OrderTagGetCreateView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('<int:pk>/tags', OrderTagGetCreateView.as_view(), name='order-tag-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),

]