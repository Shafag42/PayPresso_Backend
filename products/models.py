from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model('accounts.CustomUser')


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_images')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    short_desc = models.TextField()
    image = models.ImageField(upload_to='product_images')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
   

    def __str__(self):
        return self.name

class Product_detail(models.Model):
    long_desc = models.TextField()
    rating_count = models.IntegerField(max_length=5, null=True, blank=True)
    ice = models.DecimalField(max_digits=3, decimal_places=0, choices=((10, '10%'), (20, '20%'), (50, '50%'), (100, '100%')))
    sugar = models.DecimalField(max_digits=3, decimal_places=0, choices=((10, '10%'), (50, '50%'), (100, '100%')))
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)

    def __str__(self):
        return self.rating_count


class Brand(models.Model):
    logo = models.ImageField(upload_to='brand_logos')
    brand_name = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    follow_count = models.IntegerField(default=0)

    def calculate_average_rating(self):
        reviews = Review.objects.filter(product__brand=self)
        if reviews.exists():
            average_rating = reviews.aggregate(models.Avg('star'))['star__avg']
            self.rating = round(average_rating, 2)
        else:
            self.rating = None
        self.save()

    def increase_follow_count(self):
        self.follow_count += 1
        self.save()
    
    def decrease_follow_count(self):
        self.follow_count -= 1
        self.save()

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.brand_name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # star = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    rating = models.ForeignKey(Brand, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # def is_purchased_by(self, user):
    #   return Order.objects.filter(user=user, product=self).exists()

    # def save(self, *args, **kwargs):
    #     if not self.product.is_purchased_by(self.user):
    #         raise ValueError("You can only leave a review for a purchased product.")
    #     super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.comment




