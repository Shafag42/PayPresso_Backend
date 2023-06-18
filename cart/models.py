from django.db import models
from products.models import Product
from decimal import Decimal
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def name(self):
        return self.product.name

    @property
    def image(self):
        return self.product.image

    @property
    def price(self):
        return self.product.sell_price

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"


class Coupon(models.Model):
    code = models.CharField(max_length=255, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code

class OrderSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_subtotal(self):
        subtotal = 0
        carts = self.cart_set.all()
        for cart in carts:
            subtotal += cart.price * cart.quantity
        return subtotal
    
    def calculate_total(self):
        subtotal = self.calculate_subtotal()
        if self.coupon:
            discount = (subtotal * self.coupon.discount_percentage) / 100
            total = subtotal - discount
        else:
            total = subtotal
        return total

    def save(self, *args, **kwargs):
        self.sub_total = self.calculate_subtotal()
        self.total = self.calculate_total()
        super().save(*args, **kwargs)

        
    def __str__(self):
        return f"Order Summary - Total Price: {self.total_price}"

   


