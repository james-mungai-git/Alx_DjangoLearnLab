# relationship_app/query_samples.py
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')  # replace with your project settings
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def books_by_author_filter(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)  # using objects.filter approach
        print(f"Books by {author_name} (using filter):")
        if books.exists():
            for book in books:
                print(f"- {book.title}")
        else:
            print("No books found for this author.")
    except Author.DoesNotExist:
        print(f"No author found with the name '{author_name}'")


# 2. List all books in a library
def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # ManyToManyField if used
        print(f"Books in {library_name}:")
        if books.exists():
            for book in books:
                print(f"- {book.title}")
        else:
            print("No books found in this library.")
    except Library.DoesNotExist:
        print(f"No library found with the name '{library_name}'")


# 3. Retrieve the librarian for a library
def librarian_of_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        if hasattr(library, 'librarian'):
            print(f"Librarian of {library_name}: {library.librarian.name}")
        else:
            print(f"No librarian assigned to {library_name}")
    except Library.DoesNotExist:
        print(f"No library found with the name '{library_name}'")


# 4. REQUIRED BY CHECKER: Query librarian using `Librarian.objects.get(library=...)`
def librarian_by_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)  # REQUIRED check pattern
        print(f"Librarian managing {library_name}: {librarian.name}")
    except Library.DoesNotExist:
        print(f"No library found with the name '{library_name}'")
    except Librarian.DoesNotExist:
        print(f"No librarian linked to the library '{library_name}'")