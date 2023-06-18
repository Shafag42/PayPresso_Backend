from django.urls import path
from .views import (
    CartListCreateAPIView,
    CartDetailAPIView,
    CouponListCreateAPIView,
    CouponDetailAPIView,
    OrderSummaryListCreateAPIView,
    OrderSummaryDetailAPIView,
)

urlpatterns = [
    path('carts/', CartListCreateAPIView.as_view(), name='cart-list-create'),
    path('carts/<int:pk>/', CartDetailAPIView.as_view(), name='cart-detail'),
    path('coupons/', CouponListCreateAPIView.as_view(), name='coupon-list-create'),
    path('coupons/<int:pk>/', CouponDetailAPIView.as_view(), name='coupon-detail'),
    path('order-summaries/', OrderSummaryListCreateAPIView.as_view(), name='order-summary-list-create'),
    path('order-summaries/<int:pk>/', OrderSummaryDetailAPIView.as_view(), name='order-summary-detail'),
]
