from django.shortcuts import render
from .serializers import MenuItemSerializer
from rest_framework import generics
from rest_framework.views import APIView
from .models import MenuItems

# Create your views here.
class MenuItemsListView(generics.ListAPIView):
    queryset = MenuItems.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItems.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    
class MenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemSerializer