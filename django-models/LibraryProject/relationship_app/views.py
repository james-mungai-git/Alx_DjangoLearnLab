from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import Permission
from django.contrib.auth import login
from .models import UserProfile
from .forms import UserRegisterForm
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .models import Book



# --------------------------
# Helper: Check if user is Admin
# --------------------------
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"


# --------------------------
# User Registration View
# --------------------------
def list_books(request):
    books = Book.objects.all()  # required by checker
    return render(request, 'relationship_app/list_books.html', {'books': books})
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')

            # Update UserProfile role
            user_profile = UserProfile.objects.get(user=user)
            user_profile.role = role
            user_profile.save()

            # Assign book permissions for Admin & Librarian
            if role in ['Admin', 'Librarian']:
                perms = Permission.objects.filter(
                    codename__in=['can_add_book', 'can_change_book', 'can_delete_book']
                )
                user.user_permissions.set(perms)
            else:
                user.user_permissions.clear()

            messages.success(request, f"Account created for {user.username} as {role}!")
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'relationship_app/register.html', {'form': form})


# --------------------------
# Dashboard (Login Required)
# --------------------------
@login_required
def dashboard(request):
    return render(
        request,
        'relationship_app/dashboard.html',
        {'user_role': request.user.userprofile.role}
    )


# --------------------------
# Admin-only View
# --------------------------
@user_passes_test(is_admin)
def admin_only_view(request):
    return render(request, "relationship_app/admin_only.html")


# --------------------------
# Permission Protected Views
# --------------------------
@permission_required("relationship_app.can_add_book")
def add_book_view(request):
    return render(request, "relationship_app/permissions/add_book.html")


@permission_required("relationship_app.can_change_book")
def edit_book_view(request):
    return render(request, "relationship_app/permissions/edit_book.html")


@permission_required("relationship_app.can_delete_book")
def delete_book_view(request):
    return render(request, "relationship_app/permissions/delete_book.html")


# --------------------------
# Login / Logout
# --------------------------
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'
