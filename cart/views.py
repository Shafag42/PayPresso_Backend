from rest_framework import generics
from .models import Cart, Coupon, OrderSummary
from .serializers import CartSerializer, CouponSerializer, OrderSummarySerializer
from rest_framework.permissions import IsAuthenticated

class CartListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

class CouponListCreateAPIView(generics.ListCreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]

class CouponDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]

class OrderSummaryListCreateAPIView(generics.ListCreateAPIView):
    queryset = OrderSummary.objects.all()
    serializer_class = OrderSummarySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderSummaryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderSummary.objects.all()
    serializer_class = OrderSummarySerializer
    permission_classes = [IsAuthenticated]
