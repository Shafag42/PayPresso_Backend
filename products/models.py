# from django.db import models
# from django.contrib.auth import get_user_model

# PersonalUser = get_user_model('accounts.PersonalUser')
# CompanyUser = get_user_model('accounts.CompanyUser')


# # Create your models here.
# class Category(models.Model):
#     name = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='category_images')

#     def __str__(self):
#         return self.name


# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     image = models.ImageField(upload_to='product_images')
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
#     category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
#     size = models.CharField(max_length=255, choices=(('S', 'Small'), ('M', 'Medium'), ('L', 'Large')))
#     ice = models.DecimalField(max_digits=3, decimal_places=0, choices=((10, '10%'), (20, '20%'), (50, '50%'), (100, '100%')))
#     sugar = models.DecimalField(max_digits=3, decimal_places=0, choices=((10, '10%'), (50, '50%'), (100, '100%')))

#     def __str__(self):
#         return self.name
    

# class Comment(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
#     personal_user = models.ForeignKey(PersonalUser, on_delete=models.CASCADE, blank=True, null=True)
#     company_user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, blank=True, null=True)
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = 'Comment'
#         verbose_name_plural = 'Comments'

#     def __str__(self):
#         return self.text

