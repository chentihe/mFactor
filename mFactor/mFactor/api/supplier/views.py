from rest_framework import generics

from ecommerce.api.supplier.models import Supplier
from ecommerce.api.supplier.serializers import SupplierSerializer

class SupplierListView(generics.ListAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all().order_by('name')