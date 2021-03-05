from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from mFactor.api.unit.models import Unit

class CartSelectAllSerializer(serializers.Serializer):
    selected = serializers.BooleanField(label='all')

class CartUnitSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()
    selected = serializer.BooleanField()
    name = serializers.ModelSerializer()
    image = serializers.ModelSerializer()

    class Meta:
        model = Unit
        fields = ('id', 'quantity', 'name', 'image', 'price', 'selected')

    def get_name(self, instance):
        return instance.product.name
    
    def get_image(self, instance):
        image = instance.unitimage_set.order_by('-is_main').first()

        if image is None:
            return None
        
        return image.image.url

class CartSerializer(serializers.Serializer):
    sku = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=True)
    selected = serializers.BooleanField(default=True)

    def validate(self, data):
        sku = data['sku']
        try:
            unit = Unit.objects.get(sku=sku)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Unit dose not exist')

        quantity = attrs['quantity']
        if unit.num_in_stock < quantity:
            raise serializers.ValidationError('Units are not enough in stock')
        
        return data

class CartDeleteSerializer(serializers.Serializer):
    sku = serializers.CharField()

    def validate_sku(self, value):
        try:
            unit = Unit.objects.get(sku=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Unit dose not exist')

        return value