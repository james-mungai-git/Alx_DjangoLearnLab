from rest_framework import serializers
from .models import Book, Author
from datetime import date

class AuthorSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Author
        fields = "__all__"

class Bookserializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        field = "__all__"
    
    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value