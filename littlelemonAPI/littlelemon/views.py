from django.shortcuts import get_object_or_404
from .serializers import (
    RegisterUserSerializer,
    LoginSerializer,
    OrderSerializer,
    CategorySerializer,
    MenuItemSerializer,
    CartSerializer
)
from .models import Cart, Category, MenuItem, Order, OrderItem
from rest_framework import generics, permissions, status, filters,viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage


class Pagination:
    page_size = 10
    page_size_query_param = 'perpage'
    max_page_size = 50


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def menuitems(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()

        category_name = request.query_params.get('category')
        price = request.query_params.get('price')
        ordering = request.query_params.get('ordering')
        search = request.query_params.get('search')
        perpage = int(request.query_params.get('perpage', 10))
        page = int(request.query_params.get('page', 1))

        if category_name:
            items = items.filter(category__title=category_name)

        if price:
            items = items.filter(price__lte=price)

        if search:
            items = items.filter(title__icontains=search)

        if ordering:
            items = items.order_by(*ordering.split(','))

        paginator = Paginator(items, perpage)

        try:
            items = paginator.page(page)
        except EmptyPage:
            items = []

        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not request.user.is_staff:
            return Response(
                {"detail": "Not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MenuItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def singleitem(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    serializer = MenuItemSerializer(item)
    return Response(serializer.data)


class MealItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['price', 'inventory']
    search_fields = ['title', 'category__title']

    def get_permissions(self):
        if self.request.method in ['POST','PUT','PATCH','DELETE']:
            return [IsAdminUser()]
        return super().get_permissions()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cart(request):
    user = request.user
    menu_item_id = request.data.get('menu_item_id')
    quantity = int(request.data.get('quantity', 1))

    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    unit_price = menu_item.price
    price = unit_price * quantity

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        menu_item=menu_item,
        defaults={
            'unit_price': unit_price,
            'quantity': quantity,
            'price': price
        }
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.price = cart_item.unit_price * cart_item.quantity
        cart_item.save()

    serializer = CartSerializer(cart_item)

    return Response(
        {
            'message': 'Item added to cart',
            'item': serializer.data
        },
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
    )

class OrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context