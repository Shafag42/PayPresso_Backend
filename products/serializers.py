from rest_framework import serializers
from .models import Product,Product_detail # , Brand, Review
from category.serializers import CategorySerializer
from wishlists.serializers import WishlistSerializer

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    favorites = WishlistSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_detail
        fields = '__all__'



# class BrandSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Brand
#         fields = '__all__'


# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = '__all__'
