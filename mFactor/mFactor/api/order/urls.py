from django.urls import path

from mFactor.api.order.views import OrderView, OrderDetailView

urlpatterns = [
    path('orders/', OrderView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order=detail'),
]