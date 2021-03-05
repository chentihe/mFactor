from django.core.serializers import get_serializer
from rest_framework import status, generics
from rest_framework.response import Response
import logging

from mFactor.api.cart.utils import CartMixin
from mFactor.api.unit.models import Unit
from mFactor.api.cart.serializers import CartSerializer, CartUnitSerializer, CartDeleteSerializer, CartSelectAllSerializer

logger = logging.getLogger('django')

class CartSelectAllView(CartMixin, generics.GenericAPIView):
    serializer_class = CartSelectAllSerializer

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        selected = serializer.validated_data['selected']

        cart_dict = self.get_cart(request)

        for sku_key in cart_dict:
            cart_dict[sku_key][1] = True

        response = Response(serializer.data)
        self.post_cart(request, cart_dict, response)

        return response

class CartView(CartMixin, generics.GenericAPIView):
    serializer_class = CartSerializer

    def get(self, request):
        cart_dict = self.get_cart(request)

        sku_list = cart_dict.keys()
        skus = list()

        try:
            skus = Unit.objects.filter(sku__in=sku_list)
        except Exception as e:
            logger.error(f'Query Error:[message: {e}]')

        for sku in skus:
            sku.quantity = cart_dict[sku][0]
            sku.selected = cart_dict[sku][1]

        serializer = CartUnitSerializer(skus, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attrs = serializer.validated_data
        sku, quantity, selected = attrs['sku'], attrs['quantity'], attrs['selected']

        cart_dict = self.get_cart(request)

        cart_dict[sku] = [quantity, selected]

        response = Response(serializer.data)
        self.post_cart(request, cart_dict, response)

        return response

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attrs = serializer.validated_data
        sku, quantity, selected = attrs['sku'], attrs['quantity'], attrs['selected']

        cart_dict = self.get_cart(request)

        cart_dict[sku] = [quantity, selected]

        response = Response(serializer.data)
        self.post_cart(request, cart_dict, response)

        return response

    def delete(self, request):
        serializer = CartDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sku = serializer.validated_data['sku']

        cart_dict = self.get_cart(request)

        try:
            cart_dict.pop(sku)
        except Exception:
            return Response({'message': 'Unit is not in cart'}, status=status.HTTP_404_NOT_FOUND)

        response = Response(serializer.data)
        self.post_cart(request, cart_dict, response)