from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    menuitems,
    singleitem,
    MealItemView,
    cart,
    OrderView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('menuitems/', menuitems, name='menuitems'),              
    path('menuitems/<int:pk>/', singleitem, name='singleitem'),   
    path('mealitems/', MealItemView.as_view(), name='mealitems'), 
    path('cart/', cart, name='cart'),                            
    path('orders/', OrderView.as_view(), name='orders'),          
]