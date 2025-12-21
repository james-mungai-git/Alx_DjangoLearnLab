from django.urls import path, include
from .views import MenuItemsView, MenuItemView,MenuItemsListView

urlpatterns = [
    path('menu-items/',MenuItemsView.as_view()),
    path('menu-items/<int:pk>', MenuItemView.as_view()),
    path('list-menu-items/',MenuItemsListView.as_view())
]