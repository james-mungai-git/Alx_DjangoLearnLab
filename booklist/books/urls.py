from django.urls import path
from . import views
from .views import BookList,Book

urlpatterns = [
    path('books/',BookList.as_view()),
    path ('books/<int:pk>',Book.as_view()),
]