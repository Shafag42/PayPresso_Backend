from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from .models import Category
from .serializers import CategorySerializer

# Create your views here.

class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = []
    permission_classes = [AllowAny]

class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # authentication_classes = []
    # permission_classes = [AllowAny]
