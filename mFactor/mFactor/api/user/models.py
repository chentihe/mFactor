from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    GENDER_CHOICES = (
        ('male', u'male'),
        ('female', u'female')
    )

    user = models.OneToOneField(to=User, on_delete=models.CASCADE,
                                related_name='profile')
    phone = models.CharField(max_length=10, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='female')

class DeliveryInfo(models.Model):
    user = models.OneToOneField(to=UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    city = models.CharField(max_length=100, default='')
    district = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=10)

class UserBody(models.Model):
    user = models.OneToOneField(to=UserProfile, on_delete=models.CASCADE)
    height = models.PositiveIntegerField(max_length=3)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    breast = models.DecimalField(max_digit=5, decimal_places=2)
    waist = models.DecimalField(max_digit=5, decimal_places=2)
    hip = models.DecimalField(max_digit=5, decimal_places=2)
    shoes = models.DecimalField(max_digit=5, decimal_places=2)
