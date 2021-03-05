from django.db import models

from ecommerce.api.user.models import User
from ecommerce.api.unit.models import Unit

class Order(models.Model):
    unit_set = models.ManyToManyField(to=Unit, through='OrderUnit')
    user = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        items_count = self.unit_set.all().count()
        return 'Order ({} items) by {}'.format(items_count, self.name)