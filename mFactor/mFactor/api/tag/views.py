from rest_framework import generics

from mFactor.api.tag.models import Tag
from mFactor.api.tag.serializers import TagSerializer

class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer