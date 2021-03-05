from django import forms
from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin
from django.core.exceptions import ValidationError

from restshop.api.order.models import Order
from restshop.api.order_unit.models import OrderUnit
from restshop.api.product.models import Product
from restshop.api.unit.models import Unit, UnitImage
from restshop.api.user.models import Supplier

SUPPLIER_LOOKUPS = {
    'unit': {
        'lookup': 'product__supplier',
        'model': Unit
    },
    'unit_set': {
        'lookup': 'product__supplier',
        'model': Unit
    },
    'unitimage': {
        'lookup': 'unit_set__product__supplier',
        'model': UnitImage
    },
    'product': {
        'lookup': 'supplier',
        'model': Product
    },
    'order': {
        'lookup': 'unit_set__product__supplier',
        'model': Order
    },
    'orderunit': {
        'lookup': 'unit__product__supplier',
        'model': OrderUnit
    },
}

def get_supplier(request):
    return Supplier.objects.get(user=request.user)

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'

    def clean_value_set(self):
        values = self.cleaned_data.get('value_set')

        '''
        同一規格會有不同尺寸(顏色: 黑, 顏色: 白)
        不能對應同一個unit
        '''
        properties = []
        if values:
            for value in values.all():
                if value.property.id not in properties:
                    properties.append(value.property.id)
                else:
                    if value.property.name != 'Color':
                        raise ValidationError(
                        'Unit property {} has multiple values'.format(value.property.name)
                    )
        return values

class QuerysetForSupplierMixin(BaseModelAdmin):

    def set_filtered_queryset(self, db_field, request, kwargs):
        supplier = get_supplier(request)

        for field in SUPPLIER_LOOKUPS:
            if db_field.name == field:
                model = SUPPLIER_LOOKUPS[field]['model']
                lookup_kwargs = {SUPPLIER_LOOKUPS[field]['lookup']: supplier}
                kwargs['queryset'] = model.objects.filter(**lookup_kwargs).distinct()
        
        if db_field.name == 'supplier':
            kwargs['queryset'] = Supplier.objects.filter(id=supplier.id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            self.set_filtered_queryset(db_field, request, kwargs)

        return super(QuerysetForSupplierMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            self.set_filtered_queryset(db_field, request, kwargs)

        return super(QuerysetForSupplierMixin, self).formfield_for_manytomany(db_field, request, **kwargs)

class OrderUnitInline(QuerysetForSupplierMixin, admin.StackedInline):
    model = OrderUnit
    extra = 1
    can_delete = False

    def get_max_num(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return super(OrderUnitInline, self).get_max_num(request, obj, **kwargs)

        return 0

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields + ('unit', 'quantity', 'unit_price')

class UnitImageInline(QuerysetForSupplierMixin, admin.StackedInline):
    model = UnitImage.unit_set.through
    extra = 1

class PropertyAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.get_readonly_fields

        return self.readonly_fields + ('name',)

class PropertyValueAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields

        return self.readonly_fields + ('property', 'value')