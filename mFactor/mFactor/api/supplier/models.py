from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=128, blank=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to='supplier_image/')

    def __str__(self):
        return self.name