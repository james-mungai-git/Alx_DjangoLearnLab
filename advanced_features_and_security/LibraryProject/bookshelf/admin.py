from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usermodel
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usermodel
        fields = ("email", "username", "date_of_birth", "profile_photo")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Usermodel
        fields = ("email", "username", "date_of_birth", "profile_photo",
                  "is_active", "is_staff", "is_superuser")


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Usermodel

    list_display = ("email", "username", "date_of_birth", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal Info", {"fields": ("date_of_birth", "profile_photo")}),
        ("Permissions", {"fields": (
            "is_active", "is_staff", "is_superuser", "groups", "user_permissions"
        )}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "date_of_birth", "profile_photo",
                       "password1", "password2", "is_staff", "is_active")}
        ),
    )

    search_fields = ("email", "username")
    ordering = ("email",)


admin.site.register(Usermodel, CustomUserAdmin)
