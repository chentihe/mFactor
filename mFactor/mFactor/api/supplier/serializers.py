from rest_framework import serializers

from ecommerce.api.supplier.models import Supplier

class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = ('name')