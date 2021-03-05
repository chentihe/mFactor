from rest_framework import serializers

from mFactor.api.supplier.models import Supplier

class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = ('name')