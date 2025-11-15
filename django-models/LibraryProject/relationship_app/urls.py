# relationship_app/urls.py
from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view URL
    path('books/', views.list_books, name='list_books'),
    
    # Class-based view URL
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Additional URLs (bonus)
    path('author/<int:author_id>/', views.author_books, name='author_books'),
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    
    # Home page for the app
    path('', views.LibraryListView.as_view(), name='home'),
]