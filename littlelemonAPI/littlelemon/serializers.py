from rest_framework import serializers
from .models import MenuItems,Category
from decimal import Decimal

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax= serializers.SerializerMethodField(method_name='tax')
    category = serializers.StringRelatedField()
    class Meta:
        model = MenuItems
        fields = ["id","title","price", "stock","price_after_tax","category"]
        
    def tax(self, product:MenuItems):
        return product.price * Decimal(1.1)