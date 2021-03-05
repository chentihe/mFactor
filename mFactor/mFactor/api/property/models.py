from django.db import models

class Property(models.Model):
    '''規格分類(例如：西裝外套顏色)'''
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    '''後台管理若規格分類為複數時顯示的名稱'''
    class Meta:
        verbose_name_plural = 'properties'

class PropertyValue(models.Model):
    '''
    Property : 顏色
    Value : 藍色
    '''
    property = models.ForeignKey(to=Property, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        ordering = ['property__name', 'value']

    def __str__(self):
        return '{}: {}'.format(self.property.name, self.value)