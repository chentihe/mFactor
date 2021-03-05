from django.db import models

from mFactor.api.tag import Tag
from mFactor.api.category import Category
from mFactor.api.supplier import Supplier

class Product(models.Model):
    '''
    產品大類(例如：西裝外套)
    SPU : Standard Product Unit
    '''
    name = models.CharField(max_length=255)
    tag_set = models.ManyToManyField(to=Tag)
    supplier = models.ForeignKey(to=Supplier)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name