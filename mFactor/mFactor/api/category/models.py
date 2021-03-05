from django.db import models

from ecommerce.api.supplier.models import Supplier
from ecommerce.api.product.models import Product

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey('self', blank=True, null=True, related_name='child_category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name