from rest_framework import generics

from ecommerce.api.tag.models import Tag
from ecommerce.api.tag.serializers import TagSerializer

class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer