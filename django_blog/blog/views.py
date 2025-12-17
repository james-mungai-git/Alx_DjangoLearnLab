from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import Register, PostForms, CommentForm
from .models import Post, Comment
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
              

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

class PostCreateView(CreateView):
    model = Post  
    form_class = PostForms  
    template_name = "blog/blog_post.html"
    success_url = reverse_lazy('home')  
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = "blog/blog_post.html"  
    success_url =  reverse_lazy('home')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
 

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'  
    success_url = reverse_lazy('home')

    def get_object(self):
        obj = super().get_object()
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj

@login_required(login_url='/login/')


def home(request):
    posts = Post.objects.all().order_by('published_date')  
    
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        Post.objects.filter(id=post_id, author=request.user).delete()
        messages.success(request, "Post deleted successfully!")
        return redirect("home")

    return render(request, "blog/home.html", {"posts": posts})

def profile(request):
    return render(request, "blog/profile.html")

def register(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
    else:
        form = Register()

    return render(request, "blog/register.html", {"form": form})

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("/login/")

# coomment views

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/post-comment.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        # redirect to the post detail page after submission
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pass the post to the template
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context



class CommentDetailView(DetailView):
    model = Comment
    template_name = "blog/comment-detail.html"  
    context_object_name = 'comments'
    

class CommentListView(ListView):
    model = Comment
    template_name = "blog/comment-list.html"  
    context_object_name = 'comments'


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = "blog/post-comment.html" 
    fields = ['content']  
    success_url = reverse_lazy("post-detail")
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_delete.html"  
    success_url = reverse_lazy("post-detail")
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
