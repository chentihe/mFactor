from rest_framework import generics

from ecommerce.api.property.models import Property
from ecommerce.api.property.serializers import PropertySerializer

class PropertyListView(generics.ListAPIView):
    '''僅顯示產品規格清單'''
    queryset = Property.objects.all()
    serializer_class = PropertySerializer