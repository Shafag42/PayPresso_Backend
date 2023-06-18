from rest_framework import serializers
from .models import Cart, Coupon, OrderSummary

class CartSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='product.name')
    image = serializers.ReadOnlyField(source='product.image')
    price = serializers.ReadOnlyField(source='product.sell_price')

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity', 'name', 'image', 'price']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class OrderSummarySerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    coupon = CouponSerializer()

    class Meta:
        model = OrderSummary
        fields = ['id', 'user', 'cart', 'sub_total', 'vat', 'coupon', 'total']
