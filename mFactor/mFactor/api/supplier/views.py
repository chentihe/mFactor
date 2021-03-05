from rest_framework import generics

from mFactor.api.supplier.models import Supplier
from mFactor.api.supplier.serializers import SupplierSerializer

class SupplierListView(generics.ListAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all().order_by('name')