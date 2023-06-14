from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics,filters
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Category,Product,Product_detail,Favorite
from .serializers import CategorySerializer,ProductSerializer,ProductDetailSerializer,FavoriteSerializer
# Create your views here.


class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = []
    permission_classes = [AllowAny]

class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'short_desc']  # Specify the fields you want to enable search on
    
    def get_queryset(self):
        query = self.request.query_params.get('search', '')
        queryset = Product.objects.all()

        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(category__name__icontains=query))

        return queryset


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'  # Lookup alanını slug olarak ayarla

class ProductDetailListAPIView(generics.ListAPIView):
    queryset = Product_detail.objects.all()
    serializer_class = ProductDetailSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

# get_related_products
    def get_queryset(self):
        product_slug = self.kwargs['product_slug']
        product = get_object_or_404(Product, slug=product_slug)
        return product.related_products.all()


class ProductDetailRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product_detail.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_object(self):
        product_slug = self.kwargs['slug']
        return get_object_or_404(Product, slug=product_slug)


#category products
class CategoryProductsAPIView(ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Product.objects.filter(category__slug=slug)


class FavoriteListAPIView(generics.ListAPIView):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)
    

class FavoriteCreateAPIView(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    
class FavoriteDeleteAPIView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer