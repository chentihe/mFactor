from django.contrib import admin

from mFactor.api.category.models import Category
from mFactor.api.order.models import Order
from mFactor.api.order_unit.models import OrderUnit
from mFactor.api.product.models import Product
from mFactor.api.property.models import Property, PropertyValue
from mFactor.api.supplier.models import Supplier
from mFactor.api.tag.models import Tag
from mFactor.api.unit.models import Unit, UnitImage
from mFactor.api.user.models import DeliveryInfo, UserBody, UserProfile
from mFactor.admin_models import PropertyAdmin, PropertyValueAdmin

admin.site.register(Category)
admin.site.register([Supplier, Tag])
admin.site.register(PropertyValue, PropertyValueAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Unit)
admin.site.register(Product)
admin.site.register(UnitImage)
admin.site.register(Order)
admin.site.register(OrderUnit)