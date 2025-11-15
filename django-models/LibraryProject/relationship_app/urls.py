from django.urls import path
from . import views

urlpatterns = [
    path('', views.library_list, name='library_list'),
    path('library/<int:pk>/', views.library_detail, name='library_detail'),

    # Book CRUD
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
]
