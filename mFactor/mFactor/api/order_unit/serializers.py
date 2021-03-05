from rest_framework import serializers

from ecommerce.api.order_unit.models import OrderUnit
from ecommerce.api.unit.serializers import UnitForOrderDetail

class OrderUnitSerializer(serializers.ModelSerializer):
    unit = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = OrderUnit
        fields = ('quantity', 'status', 'unit')

    def get_unit(self, obj):
        data = UnitForOrderDetail(obj.unit).data

        '''以當時價格為準，避免產品更改價格導致取到不對的價格'''
        data['price'] = obj.unit_price

        return data

    def get_status(self, obj):
        return obj.get_status_display()