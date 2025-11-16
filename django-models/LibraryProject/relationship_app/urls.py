from django.urls import path
from .views import (
    register, dashboard, CustomLoginView, CustomLogoutView,
    admin_only_view, add_book_view, edit_book_view, delete_book_view
)

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("dashboard/", dashboard, name="dashboard"),

    # Admin exclusive
    path("admin-only/", admin_only_view, name="admin_only"),

    # Book permission views
    path("books/add/", add_book_view, name="add_book"),
    path("books/edit/", edit_book_view, name="edit_book"),
    path("books/delete/", delete_book_view, name="delete_book"),
]
