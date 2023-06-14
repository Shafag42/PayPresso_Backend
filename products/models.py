from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_images')
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    short_desc = models.TextField()
    image = models.ImageField(upload_to='product_images')
    orginal_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField()
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    related_products = models.ManyToManyField('self', blank=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True)


    @property
    def discounted_price(self):
        return ((self.orginal_price)*(self.discount))/100

    @property
    def sell_price(self):
        return (self.orginal_price)-(self.discounted_price)
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.name

class Product_detail(models.Model):
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    long_desc = models.TextField()
    rating_count = models.IntegerField(null=True, blank=True)
    ice = models.DecimalField(max_digits=3, decimal_places=0, choices=((10, '10%'), (20, '20%'), (50, '50%'), (100, '100%')))
    sugar = models.DecimalField(max_digits=3, decimal_places=0, choices=((10, '10%'), (50, '50%'), (100, '100%')))
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.rating_count)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.long_desc
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return self.product.name


# class Brand(models.Model):
#     logo = models.ImageField(upload_to='brand_logos')
#     brand_name = models.CharField(max_length=100)
#     rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)
#     follow_count = models.IntegerField(default=0)

#     def calculate_average_rating(self):
#         reviews = Review.objects.filter(product__brand=self)
#         if reviews.exists():
#             average_rating = reviews.aggregate(models.Avg('star'))['star__avg']
#             self.rating = round(average_rating, 2)
#         else:
#             self.rating = None
#         self.save()

#     def increase_follow_count(self):
#         self.follow_count += 1
#         self.save()
    
#     def decrease_follow_count(self):
#         self.follow_count -= 1
#         self.save()

#     class Meta:
#         verbose_name = 'Brand'
#         verbose_name_plural = 'Brands'

#     def __str__(self):
#         return self.brand_name


# class Review(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='user_images')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     # star = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
#     rating = models.ForeignKey(Brand, on_delete=models.CASCADE)
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)

    # def is_purchased_by(self, user):
    #   return Order.objects.filter(user=user, product=self).exists()

    # def save(self, *args, **kwargs):
    #     if not self.product.is_purchased_by(self.user):
    #         raise ValueError("You can only leave a review for a purchased product.")
    #     super().save(*args, **kwargs)


    # class Meta:
    #     verbose_name = 'Review'
    #     verbose_name_plural = 'Reviews'

    # def __str__(self):
    #     return self.comment




