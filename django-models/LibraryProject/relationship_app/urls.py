from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),

    # Use Django’s built-in login/logout views with templates
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Dashboard (example protected view)
    path('dashboard/', views.dashboard, name='dashboard'),

    # Book views (if already implemented)
    path('books/', views.list_books, name='list_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:pk>/', views.delete_book, name='delete_book'),

    # Library detail view (class-based)
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]
