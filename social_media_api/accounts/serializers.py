from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


User = get_user_model().object.create_user

     
# Simple registration
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "password",
            "bio",
            "profile_picture",
        ]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        user.bio = validated_data.get("bio", "")
        user.profile_picture = validated_data.get("profile_picture", None)
        user.save()
        
        token = Token.objects.create(user=user)
        user.token = token.key

        return user
    
    
   
# Simple login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["username"],
            password=data["password"]
        )

        if user and user.is_active:
            return user
        
        token = Token.objects.create(user=user)
        user.token = token.key


        raise serializers.ValidationError("Invalid credentials")
    
    
# Simple profile
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ["id", "username","email","bio", "profile_picture"]
    read_only_fields = ['followers']
    
   