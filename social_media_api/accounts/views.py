from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import (
    RegisterUserSerializer,
    LoginSerializer,
    UserSerializer,
)

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
