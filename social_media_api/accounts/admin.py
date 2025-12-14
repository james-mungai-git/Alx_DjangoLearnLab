from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'get_followers_count']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio', 'profile_picture', 'followers')}),
    )
    
    def get_followers_count(self, obj):
        return obj.get_followers_count()
    get_followers_count.short_description = 'Followers Count'


admin.site.register(User, CustomUserAdmin)