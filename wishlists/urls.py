from django.urls import path
from .views import WishlistListAPIView, WishlistCreateAPIView, WishlistDeleteAPIView

urlpatterns = [
    # Other URL patterns
    path('wishlists/', WishlistListAPIView.as_view(), name='wishlist-list'),
    path('wishlists/add/', WishlistCreateAPIView.as_view(), name='wishlists-create'),
    path('wishlists/<int:pk>/delete/', WishlistDeleteAPIView.as_view(), name='wishlist-delete'),
]