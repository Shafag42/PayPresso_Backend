from django.urls import path
from .views import (CategoryProductsAPIView,
                    ProductDetailAPIView,ProductDetailsAPIView,
                    ProductListAPIView,ProductDetailsListAPIView )

urlpatterns = [
    
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('product-details/', ProductDetailsListAPIView.as_view(), name='product-detail-list'),
    path('product-details/<slug:slug>/', ProductDetailsAPIView.as_view(), name='product-detail-detail'),
    path('product-details/<slug:slug>/update/', ProductDetailsAPIView.as_view(), name='product-detail-update'),
    path('categories/<slug:slug>/products/', CategoryProductsAPIView.as_view(), name='category-products'), #categoryproducts
    path('products/<slug:product_slug>/related/', ProductDetailsListAPIView.as_view(), name='related-products'),
    
]                                                                                                                                                                                                                                         
