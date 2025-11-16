# relationship_app/query_samples.py
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')  # replace with your project settings
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
def books_by_author_filter(author_name):
    """
    Returns a queryset of books written by the specified author.
    If the author does not exist, returns None.
    """
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)  # required filter query
        return books
    except Author.DoesNotExist:
        return None


# 2. List all books in a library
def books_in_library(library_name):
    """
    Returns all books inside the specified library.
    If the library does not exist, returns None.
    """
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return None


# 3. Retrieve the librarian for a library
def librarian_of_library(library_name):
    """
    Returns the librarian assigned to the specified library.
    If library or librarian does not exist, returns None.
    """
    try:
        library = Library.objects.get(name=library_name)
        return getattr(library, 'librarian', None)
    except Library.DoesNotExist:
        return None
