from django.urls import path
from .views import CategoryListAPIView, CategoryDetailAPIView

urlpatterns = [
    # Other URL patterns
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    
]