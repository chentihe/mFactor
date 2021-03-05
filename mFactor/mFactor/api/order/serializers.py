from rest_framework import serializers


from mFactor.api.order.models import Order, OrderUnit
from mFactor.api.unit.models import Unit
from mFactor.api.order_unit.serializers import OrderUnitSerializer
from mFactor.api.cart.utils import CartMixin

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'name', 'address', 'phone')               

class OrderListSerializer(serializers.ModelSerializer):
    unit_num = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'created_at', 'units_num')

    def get_unit_num(self, obj):
        return obj.unit_set.count()

class OrderDetailSerializer(serializers.ModelSerializer):
    units = OrderUnitSerializer(
        many=True,
        read_only=True,
        source='orderunit_set'
    )

    class Meta:
        model = Order
        fields = ('id', 'created_at', 'name', 'address', 'phone', 'units')