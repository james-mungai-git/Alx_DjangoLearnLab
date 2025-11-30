from rest_framework import viewsets
from .serializers import BookSerializer, AuthorSerializer
from .models import Book, Author

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all
    serializer_class = AuthorSerializer