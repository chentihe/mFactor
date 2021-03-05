from django.db import models

from ecommerce.api.product.models import Product
from ecommerce.api.property.models import PropertyValue

class Unit(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    value_set = models.ForeignKey(to=PropertyValue)
    sku = models.CharField(max_length=255, primary_key=True)
    price = models.PositiveIntegerField()
    num_in_stock = models.PositiveIntegerField(default=5)
    on_sale = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(blank=True)

    class Meta:
        ordering = ['product__name', 'sku']

    def __str__(self):
        properties = ', '.join(str(value) for value in self.value_set.all())
        return '{}: {}'.format(self.product.name, properties)

class UnitImage(models.Model):
    '''同顏色有不同尺寸，unit可以共用圖片，所以使用ManyToMany'''
    unit_set = models.ManyToManyField(to=Unit, blank=True)
    image = models.ImageField(upload_to='product_images/')
    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = ['image']

    def __str__(self):
        unit = self.unit_set.first()
        if unit is not None:
            product_name = unit.product.name
        else:
            product_name = 'No unit assigned'

        return '{}: {}'.format(product_name, self.image.name)

    def delete(self, *args, **kwargs):
        self.image.delete()

        super(UnitImage, self).delete(*args, **kwargs)