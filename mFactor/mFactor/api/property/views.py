from rest_framework import generics

from mFactor.api.property.models import Property
from mFactor.api.property.serializers import PropertySerializer

class PropertyListView(generics.ListAPIView):
    '''僅顯示產品規格清單'''
    queryset = Property.objects.all()
    serializer_class = PropertySerializer