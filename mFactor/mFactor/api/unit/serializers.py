from rest_framework import serializers

from mFactor.api.unit.models import Unit

class UnitSerializer(serializers.ModelSerializer):
    properties = serialzers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('sku', 'price', 'discount', 'properties', 'images', 'num_in_stock')

    def get_properties(self, obj):
        return [{
            'name': property_value.property.name,
            'value': property_value.value
        } for porperty_value in obj.value_set.all()]

    def get_images(self, obj):
        images = obj.unitimage_set.all()

        if images.exists():
            return [image.image.url for image in images.all()]

        else:
            return []

    def get_discount(self, obj):
        if obj.on_sale:
            return obj.discount
        else:
            return ['this product is not on sale.']

class UnitForOrderDetail(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name')
    properties = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    product_id = serializers.IntegerField(source='product.id')

    class Meta:
        model = Unit
        fields = ('name', 'properties', 'image', 'product_id', 'price', 'discount', 'sku', 'num_in_stock')

    def get_properties(self, obj):
        return [{
            'name': property_value.property.name,
            'value': property_value.value
        } for porperty_value in obj.value_set.all()]

    def get_image(self, obj):
        image = obj.unitimage_set.order_by('-is_main').first()

        if image is None:
            return None

        return image.image.url

    def get_discount(self, obj):
        if obj.on_sale:
            return obj.discount
        else:
            return ['this product is not on sale.']