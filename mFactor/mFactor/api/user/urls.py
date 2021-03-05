from django.urls import path
from rest_framework_sav.views import session_auth_view

from mFactor.api.user.views import UserView, UserCreateView, ChangePasswordView, DeliveryInfoCreateView, DeliveryInfoRUDView, UserBodyCreateView, UserBodyRUView

urlpatterns = [
    path('user/', UserView.as_view(), name='user'),
    path('user/create/', UserCreateView.as_view(), name='user-create'),
    path('deliveryinfo/', DeliveryInfoRUDView.as_view(), name='user-address'),
    path('auth/', session_auth_view, name='auth'),
    path('password/', ChangePasswordView.as_view(), name='change-password'),
    path('user/<int:pk>/bodyinfo/create/', UserBodyCreateView.as_view(), name='bodyinfo-create'),
    path('user/<int:pk>/bodyinfo/', UserBodyRUView.as_view(), name='user-bodyinfo'),
]