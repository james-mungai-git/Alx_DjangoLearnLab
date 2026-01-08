from rest_framework import serializers
from .models import MenuItems,Category
from decimal import Decimal
from rest_framework.validators import UniqueValidator
import bleach # type: ignore


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","slug","title"]
 
class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax= serializers.SerializerMethodField(method_name='tax')
    category = CategorySerializer(read_only=True)
    title = serializers.CharField(max_length=255, 
                                  validators=[UniqueValidator(queryset=MenuItems.objects.all())])
    def validate_title(self, value):
        return bleach.clean(value)
   
    class Meta:
        model = MenuItems
        fields = ["id","title","price", "stock","price_after_tax","category"]
        extra_kwargs={
            'price': {'min_value':2},
            'stock': {'source':'inventory', 'min_value':0}
        }
        
    def tax(self, product:MenuItems):
        return round(product.price * Decimal(1.1),2) 

    
    def menu_items(request, items):
        serialized_item = MenuItemSerializer(items, many=True, context={'request': request})