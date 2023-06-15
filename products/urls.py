from django.urls import path
from .views import (CategoryListAPIView, CategoryDetailAPIView,CategoryProductsAPIView,
                    ProductDetailAPIView,ProductDetailsAPIView,
                    ProductListAPIView,ProductDetailsListAPIView,
                    FavoriteListAPIView,FavoriteCreateAPIView,FavoriteDeleteAPIView)

urlpatterns = [
    # Other URL patterns
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('product-details/', ProductDetailsListAPIView.as_view(), name='product-detail-list'),
    path('product-details/<slug:slug>/', ProductDetailsAPIView.as_view(), name='product-detail-detail'),
    path('product-details/<slug:slug>/update/', ProductDetailsAPIView.as_view(), name='product-detail-update'),
    path('categories/<slug:slug>/products/', CategoryProductsAPIView.as_view(), name='category-products'), #categoryproducts
    path('favorites/', FavoriteListAPIView.as_view(), name='favorite-list'),
    path('favorites/add/', FavoriteCreateAPIView.as_view(), name='favorite-create'),
    path('favorites/<int:pk>/delete/', FavoriteDeleteAPIView.as_view(), name='favorite-delete'),
    path('products/<slug:product_slug>/related/', ProductDetailsListAPIView.as_view(), name='related-products'),
    
]                                                                                                                                                                                                                                         
