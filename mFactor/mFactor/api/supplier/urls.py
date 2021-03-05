from django.urls import path

from mFactor.api.supplier.views import SupplierListView

urlpatterns = [
    path('suppliers/', SupplierListView.as_view(), name='supplier-list'),
]