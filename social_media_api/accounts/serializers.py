from rest_framework import serializers
from . models import User
from django.contrib.auth import authenticate

     
# Simple registration
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "bio",
            "profile_picture",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        user.bio = validated_data.get("bio", "")
        user.profile_picture = validated_data.get("profile_picture", None)
        user.save()

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

        raise serializers.ValidationError("Invalid credentials")
    
    
# Simple profile
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "username","email","bio", "profile_picture"]
    read_only_fields = ['followers']
