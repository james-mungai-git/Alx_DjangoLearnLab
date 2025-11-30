from django.urls import path
from .views import (
    BookListView,
    BookDetailView, 
    BookCreateView,
    BookUpdateView,  # Make sure this is imported
    BookDeleteView   # Make sure this is imported
)

urlpatterns = [
    # List all books
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Get single book details
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Create new book
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # Update existing book - ADD THIS
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    
    # Delete book - ADD THIS
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]