from rest_framework import serializers

from ecommerce.api.category.models import Category

class CatergorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'parentid', 'subcategories')

    def get_fields(self):
        fields = super(CatergorySerializer, self).get_fields()
        fields['subcategories'] = CatergorySerializer(many=True)
        return fields