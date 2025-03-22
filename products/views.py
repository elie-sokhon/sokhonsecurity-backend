from rest_framework import generics, filters
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import AllowAny

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']  # Search by name or description

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer





