from django.urls import path

from mFactor.api.cart.views import CartView, CartSelectAllView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/selection/', CartSelectAllView.as_view(), name='cart-selectall'),
]