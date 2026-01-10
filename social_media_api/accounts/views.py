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
    
 
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_users(request):
    users = CustomUser.objects.all()   
    data = [{"id": u.id, "username": u.username} for u in users]
    return Response(data)

   
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




















from django.shortcuts import render
from .serializers import MenuItemSerializer
from .models import MenuItems, Category
from rest_framework.decorators import api_view,renderer_classes, permission_classes, throttle_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from django.core.paginator import Paginator, EmptyPage
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group


# Create your views here.

@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItems.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        price = request.query_params.get('price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', 2)
        page = request.query_params.get('page', 1)

        if category_name:
            items = items.filter(category__title=category_name)
        if price:
            items = items.filter(price__lte=price)
        if search:
            items = items.filter(title__icontains=search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        paginator = Paginator(items, per_page=perpage)

        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []

        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data)

    elif request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()

        limit = int(request.query_params.get('limit', 5))  
        items = MenuItems.objects.all()[:limit]

        data = [
            {
                'id': item.id,
                'title': item.title,
                'price': item.price,
                'inventory': item.inventory
            }
            for item in items
        ]

        return Response(data, status=status.HTTP_201_CREATED)
    
    
@api_view()
def single_item(request,pk):
    item = get_object_or_404(MenuItems, pk=pk)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)


@api_view()
@renderer_classes([TemplateHTMLRenderer])
def menu(request):
    items = MenuItems.objects.select_related('category').all()
    serializer = MenuItemSerializer(items, many=True)
    return Response({'data': serializer.data}, template_name='littlelemon/menu-item.html')

class MealItemViewSet(generics.ListCreateAPIView):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemSerializer 
    ordering_fields = ["price", "inventory"]
    search_fields=['title', 'category__title']
    throttle_classes=[AnonRateThrottle, UserRateThrottle]

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({'message':'some secret message'})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='manager').exists():
        return Response({'message':'only manager can view this'})
    else:
        return Response({'message':'you are not authenticated'},status=403)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
   username=request.data.get('username')
   if username:
        user = get_object_or_404(User, username=username)

        managers, created = Group.objects.get_or_create(name='manager')
        
        if request.method =='POST':
            managers.user_set.add(user)
            return Response(
                {'message': f'{username} authenticated and added to manager group'},
                status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            managers.uset_set.remove(user)
            return Response({'message':f'{username} removed from the manager group'})    

   
   return Response({'message':'error'}, status.HTTP_400_BAD_REQUEST)


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('littlelemon.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
