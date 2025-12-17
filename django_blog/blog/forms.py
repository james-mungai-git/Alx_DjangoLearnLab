from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment


class Register(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2",]

class PostForms(forms.ModelForm):
    class Meta:
        model = Post

        fields = ["title", "content"]   
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write a comment...'
            })
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 50:
            raise forms.ValidationError("Comment must be at least 50 characters.")
        return content