from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.models import Permission
from .models import UserProfile, Book, Author
from .forms import UserRegisterForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import login", "from django.contrib.auth.forms import UserCreationForm

"""
---------------------------------------------------------
 ROLE CHECK FUNCTIONS
---------------------------------------------------------
"""
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

def is_admin_or_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role in ['Admin', 'Librarian']


"""
---------------------------------------------------------
 USER REGISTRATION (with automatic permissions)
---------------------------------------------------------
"""
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')

            # Update the UserProfile with the chosen role
            user_profile = UserProfile.objects.get(user=user)
            user_profile.role = role
            user_profile.save()

            # Automatically assign book permissions to Admin & Librarian
            if role in ["Admin", "Librarian"]:
                perms = Permission.objects.filter(
                    codename__in=["can_add_book", "can_change_book", "can_delete_book"]
                )
                user.user_permissions.set(perms)
            else:
                user.user_permissions.clear()

            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username} as {role}! You can now log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'relationship_app/register.html', {'form': form})


"""
---------------------------------------------------------
 ROLE-BASED VIEWS
---------------------------------------------------------
"""
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

@login_required
def dashboard(request):
    user_role = request.user.userprofile.role
    return render(request, 'relationship_app/dashboard.html', {'user_role': user_role})


"""
---------------------------------------------------------
 BOOK CRUD VIEWS (Permission protected)
---------------------------------------------------------
"""

# View all books - allowed for all logged-in users
@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})


# Add book (Admin & Librarian have permission)
@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    authors = Author.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')

        if title and author_id:
            author = Author.objects.get(id=author_id)
            Book.objects.create(title=title, author=author)
            messages.success(request, "Book added successfully!")
            return redirect('book_list')
        else:
            messages.error(request, "Both title and author are required.")
    
    return render(request, 'relationship_app/add_book.html', {"authors": authors})


# Edit book (Admin & Librarian have permission)
@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    authors = Author.objects.all()

    if request.method == 'POST':
        book.title = request.POST.get('title')
        author_id = request.POST.get('author')

        if book.title and author_id:
            book.author = Author.objects.get(id=author_id)
            book.save()
            messages.success(request, "Book updated successfully!")
            return redirect('book_list')
        else:
            messages.error(request, "Both title and author are required.")

    return render(request, 'relationship_app/edit_book.html', {"book": book, "authors": authors})


# Delete book (Admin & Librarian have permission)
@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    messages.success(request, "Book deleted successfully!")
    return redirect('book_list')
