from django.urls import path

from ecommerce.api.supplier.views import SupplierListView

urlpatterns = [
    path('suppliers/', SupplierListView.as_view(), name='supplier-list'),
]