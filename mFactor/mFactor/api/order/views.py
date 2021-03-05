from django.contrib.sessions.models import Session
from rest_framework import status, serializers, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
from django.db import transaction
import logging

from ecommerce.api.order.models import Order
from ecommerce.api.order.serializers import OrderListSerializer, OrderSerializer, OrderDetailSerializer
from ecommerce.api.order_unit.models import OrderUnit
from ecommerce.api.cart.utils import CartMixin
from ecommerce.api.user.models import DeliveryInfo
from ecommerce.api.user.service import DeliveryInfoService

logger = logging.getLogger('django')

class OrderView(CartMixin, APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        user = request.user

        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        queryset = Order.objects.filter(user=user)
        serializer = OrderListSerializer(queryset, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data

        user = request.user
        if user and user.is_authenticated:
            DeliveryInfoService.delete_by_user(request.user)
            DeliveryInfo.objects.create(**data)
        
        # 建立order物件
        order = Order.objects.create(**data)

        # 取出購物車的資料
        cart_dict = self.get_cart(request)
        sku_list = [key for key in cart_dict.keys() if cart_dict[key][1]]

        if not sku_list:
            raise serializers.ValidationError('Please add units to cart')

        with transaction.atomic():
            save_id = transaction.savepoint()

            try:

                for sku in sku_list:

                    while True:
                        sku = Unit.objects.get(sku=sku)
                        sku_quantity = cart_dict[sku][0]
                        # 建立orderunit物件
                        OrderUnit.objects.create(
                            order=order,
                            unit=sku,
                            quantity=sku_quantity
                            unit_price=sku.price
                        )

                        origin_stock = sku.num_in_stock
                        
                        if origin_stock < sku_quantity:
                            raise serializers.ValidationError('Units are not enough in stock')
                        # F('num_in_stock') 直接取出unit的庫存值做運算後更新
                        result = Unit.object.filter(sku=sku, num_in_stock=origin_stock).update(stock=F('num_in_stock') - sku_quantity)
                        
                        if result == 0:
                            continue
                        break

            except Exception as e:
                logger.error(f'Order Error:[message: {e}]')
                # 過程出現錯誤則回到savepoint
                transaction.savepoint_rollback(save_id)
                raise
            else:
                transaction.savepoint_commit(save_id)
                # 購物車返回沒有被勾選的商品
                cart_dict = {key: value for key, value in cart_dict.items() if not cart_dict[key][1]}
                self.post_to_redis(request, cart_dict)

        return Response(OrderDetailSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        user = request.user
        order = Order.object.get(pk=pk)

        if user.id != order.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializers = OrderDetailSerializer(order)
        return Response(serializers.data)