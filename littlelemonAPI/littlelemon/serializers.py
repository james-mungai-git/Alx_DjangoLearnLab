from rest_framework import serializers
from .models import MenuItem,OrderItem,Order,Category,Cart
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from django.contrib.auth import authenticate
from django.utils import timezone


class RegisterUserSerializer(serializers.ModelSerializer):
    username=serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    email=serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())] )
    password=serializers.CharField(write_only=True)
    password_confirm=serializers.CharField(write_only=True)
    
    class Meta:
        model= User
        fields=['username','email','password','password_confirm']
        validators=[UniqueTogetherValidator(queryset=User.objects.all(),
                                             fields=['username','email'])]
        
    def create(request,validated_data):
        user=user.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        
        user.save()
        token, created=Token.get_or_create(user=user)
        user.token= token.key
        
        return user
        
        
class LoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)
    
    class Meta:
        model=User
        fields=['username','password']
        
    def validate(self, data):
        user=authenticate(
            username=data['username'],
            password=data['password']
        )
        
        if user and user.is_active:
            return user
        token,created=Token.objects.get_or_create(user=user)
        user.token=token.key
        
        raise serializers.ValidationError('invaid credentials')
    
    
        

class CategorySerializer(serializers.ModelSerializer):
    title=serializers.CharField()
    slug=serializers.CharField
    
    class Meta:
        model=Category
        fields=['title','slug']

class MenuItemSerializer(serializers.ModelSerializer):
    title=serializers.CharField()
    featured=serializers.BooleanField()
    category=CategorySerializer()
    price_after_tax=serializers.SerializerMethodField()
    
    class Meta:
        model=MenuItem
        fields=['title','featured','category','price','inventory','price_after_tax']
        
        def price_after_tax(self):
        
            tax_rate = 0.16 
            return round(self.price + (self.price * tax_rate),2) 


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['user', 'status', 'delivery_crew', 'date', 'total']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            raise serializers.ValidationError("Cannot place order. Cart is empty.")

        total = sum(item.price for item in cart_items)

        order = Order.objects.create(
            user=user,
            status=False,
            total=total,
            date=timezone.now().date()
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menu_item=item.menu_item,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )

        cart_items.delete()

        return order

class CartSerializer(serializers.ModelSerializer):
    menu_item = serializers.StringRelatedField()  
    user = serializers.StringRelatedField()       

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menu_item', 'quantity', 'unit_price', 'price']
