from rest_framework import viewsets

from ecommerce.api.category.models import Category
from ecommerce.api.category.serializers import CatergorySerializer

class CategoryListView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CatergorySerializer