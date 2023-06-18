from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from products.models import Product

User = get_user_model()

# Create your models here.


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return self.product.name

