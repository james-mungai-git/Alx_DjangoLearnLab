# relationship_app/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Book, Library, Author  # Added Library import

# Function-based view to list all books
def list_books(request):
    """Function-based view to display all books"""
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    """Class-based view to display details for a specific library"""
    model = Library  # This now works because Library is imported
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Additional function-based view for author details (bonus)
def author_books(request, author_id):
    """Function-based view to display books by a specific author"""
    author = get_object_or_404(Author, id=author_id)
    books = author.books.all()
    return render(request, 'relationship_app/author_books.html', {
        'author': author,
        'books': books
    })

# Additional class-based view for all libraries (bonus)
class LibraryListView(ListView):
    """Class-based view to display all libraries"""
    model = Library  # This also needs Library import
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'