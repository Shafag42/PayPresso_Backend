from django.contrib import admin
from .models import Cart, Coupon, OrderSummary

# Register your models here.

admin.site.register(Cart)
admin.site.register(Coupon)
admin.site.register(OrderSummary)
