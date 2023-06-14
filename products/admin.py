from django.contrib import admin
from .models import Product, Category,Product_detail,Favorite
# , Brand, Review

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Product_detail)
admin.site.register(Favorite)


# admin.site.register(Brand)
# admin.site.register(Review)
