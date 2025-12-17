from django import forms
from .models import Book

# Form for creating/editing books
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn']  # adjust to your model fields
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Book title'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author name'}),
            'published_date': forms.DateInput(attrs={'type': 'date'}),
            'isbn': forms.TextInput(attrs={'placeholder': 'ISBN'}),
        }

# Form for searching books
class BookSearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Search books...'})
    )

# Example form (as specified in your assignment)
class ExampleForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Enter your message'})
    )
