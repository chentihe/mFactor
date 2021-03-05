from django.urls import path

from ecommerce.api.property.views import PropertyListView

urlpatterns = [
    path('properties/', PropertyListView.as_view(), name='property-list')
]