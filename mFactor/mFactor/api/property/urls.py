from django.urls import path

from mFactor.api.property.views import PropertyListView

urlpatterns = [
    path('properties/', PropertyListView.as_view(), name='property-list')
]