from rest_framework import serializers

from ecommerce.api.property.models import Property

class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property

    '''
    自定義序列化格式
    {
        'name': 顏色,
        'values': [
          {
            'id': 1, 'value': 紅色
          },
          {
            'id': 2, 'value': 藍色
          }
        ]
    }
    '''
    def to_representation(self, instance):
        return {
            'name': instance.name,
            'values': [{
                'id': value.id,
                'value': value.value
            } for value in instance.propertyvalue_set.all()]
        }