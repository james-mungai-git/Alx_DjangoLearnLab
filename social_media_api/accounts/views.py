from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import (
    RegisterUserSerializer,
    LoginSerializer,
    UserSerializer,
)
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.CreateAPIView):
    serializer_class= RegisterUserSerializer
    permission_classes=(permissions.AllowAny,)
    
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            "user":UserSerializer(user).data,
            "token":token.key
            
        })
        
class LoginView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    permission_classes=(permissions.AllowAny,)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({"user":UserSerializer(user).data,"token":token.key})        

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    if target_user == request.user:
        return Response({"detail": "You cannot follow yourself."}, status=400)

    request.user.following.add(target_user)
    return Response({"detail": f"You are now following {target_user.username}"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    if target_user == request.user:
        return Response({"detail": "You cannot unfollow yourself."}, status=400)

    request.user.following.remove(target_user)
    return Response({"detail": f"You unfollowed {target_user.username}"}, status=200)

