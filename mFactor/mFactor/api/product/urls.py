from django.urls import path

from mFactor.api.product.views import ProductListView, ProductDetailView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]