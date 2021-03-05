from rest_framework import viewsets

from mFactor.api.category.models import Category
from mFactor.api.category.serializers import CatergorySerializer

class CategoryListView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CatergorySerializer