from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path(
        'menu-items/',
        views.MealItemViewSet.as_view(),
        name='menu-items'
    ),
    path(
        'menu-items/<int:pk>/',
        views.MealItemViewSet.as_view(),
        name='single-item'
    ),
    path(
        'menu/',
        views.menu,
        name='menu'
    ),
    path('secret/', views.secret),
    path('auth-token/', obtain_auth_token),
    path('manager-view/', views.manager_view),
    path('groups/managers/users/', views.managers),
]
