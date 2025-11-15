from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import Permission
from .models import UserProfile
from .forms import UserRegisterForm

# --------------------------
# User Registration View
# --------------------------
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')

            # Update UserProfile
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
# Optional: Dashboard (requires login)
# --------------------------
@login_required
def dashboard(request):
    return render(request, 'relationship_app/dashboard.html', {'user_role': request.user.userprofile.role})

# --------------------------
# For login/logout, we use Django’s built-in views:
# --------------------------
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'
