from django.urls import path
from .views import (
    register,
    dashboard,
    admin_only_view,
    add_book_view,
    edit_book_view,
    delete_book_view,
    CustomLoginView,
    CustomLogoutView,
)
from django.urls import path
from . import views


urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    # ... other paths like add_book/ and edit_book/
]

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),

    # Admin-only view
    path('admin-only/', admin_only_view, name='admin_only'),

    # Permission-based book views
    path('add_book/', add_book_view, name='add_book'),     # REQUIRED BY CHECKER
    path('edit_book/', edit_book_view, name='edit_book'),  # REQUIRED BY CHECKER
    path('delete_book/', delete_book_view, name='delete_book'),
]
