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

# Create your views here.

@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItems.objects.select_related('category').all()
        category_name = request.GET.get('category')
        price = request.GET.get('price')
        search = request.GET.get('search')
        ordering = request.GET.get('ordering')
        perpage = request.GET.get('perpage' ,default=2)
        page = request.GET.get('page', default=1)

        if category_name:
            items = items.filter(category__title=category_name)
        if price:
            items = items.filter(price__lte=price)
        if search:
            items = items.filter(title__icontains=search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
        
        paginator = Paginator(items,per_page=perpage)
        
        try:
            items=paginator.page(number=page)
        except EmptyPage:
            items = []    
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data)

    elif request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()

        limit = int(request.GET.get('limit'))
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
   return Response({'message':'you are authenticated'},status=403)
