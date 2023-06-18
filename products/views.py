from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics,filters
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import login_required
from .models import Product,Product_detail
from .serializers import ProductSerializer,ProductDetailSerializer
# Create your views here.

class ProductListAPIView(generics.ListCreateAPIView):
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
    authentication_classes = []
    permission_classes = [AllowAny]

class ProductDetailsListAPIView(generics.ListCreateAPIView):
    queryset = Product_detail.objects.all()
    serializer_class = ProductDetailSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

# get_related_products
    def get_queryset(self):
        product_slug = self.kwargs['product_slug']
        product = get_object_or_404(Product, slug=product_slug)
        return product.related_products.all()


class ProductDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product_detail.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs['slug']
        return get_object_or_404(Product_detail, slug=slug)


#category products
class CategoryProductsAPIView(ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Product.objects.filter(category__slug=slug)
