from django.urls import path
from rest_framework_sav.views import session_auth_view

from ecommerce.api.user.views import UserView, UserCreateView, ChangePasswordView, DeliveryInfoCreateView, DeliveryInfoRUDView, UserBodyView

urlpatterns = [
    path('user/', UserView.as_view(), name='user'),
    path('user/create/', UserCreateView.as_view(), name='user-create'),
    path('deliveryinfo/', DeliveryInfoRUDView.as_view(), name='user-address'),
    path('auth/', session_auth_view, name='auth'),
    path('password/', ChangePasswordView.as_view(), name='change-password'),
]