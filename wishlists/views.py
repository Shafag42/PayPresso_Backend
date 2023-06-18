from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from .serializers import WishlistSerializer
# Create your views here.

class WishlistListAPIView(generics.ListAPIView):
    serializer_class = WishlistSerializer

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(user=user)
    

class WishlistCreateAPIView(generics.CreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    
class WishlistDeleteAPIView(generics.DestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer