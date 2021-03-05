from django.db.models import Max, Min
from rest_framework import serializers

from ecommerce.api.product.models import Product
from ecommerce.api.tag.serializers import TagSerializer
from ecommerce.api.supplier.serializers import SupplierSerializer
from ecommerce.api.unit.serializers import UnitSerializer

class ProductListSerializer(serializers.ModelSerializer):
    '''產品清單列表'''
    tags = TagSerializer(
        many=True,
        read_only=True,
        source='tag_set'
    )
    prices = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'tags', 'prices', 'image')

    '''針對所有西裝，取出最高&最低價'''
    def get_prices(self, instance): 
        '''
        這裡的instance.unit_set，拆成instance.unit & _set
        Unit的product是用foreign key，所以要查詢此product所有的unit
        必須使用instance.unit_set
        '''
        prices = instance.unit_set.aggregate(max=Max('price'), min=Min('price'))
        return {
            'min': prices['min'],
            'max': prices['max']
        }

    def get_image(self, instance):
        '''
        查詢product所有的unit
        對所有的unit做篩選: unitimage有資料
        取出第一個有unitimage的unit
        '''
        unit = instance.unit_set.filter(unitimage__isnull=False).first()

        if unit is None:
            return None

        # 用is_main排序，挑出第一張當封面
        image = unit.unitimage_set.order_by('-is_main').first()

        if image is None:
            return None
        
        return image.image.url

class ProductSerializer(ProductListSerializer):
    units = UnitSerializer(
        many=True,
        read_only=True,
        source='unit_set'
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'tags', 'description', 'units')