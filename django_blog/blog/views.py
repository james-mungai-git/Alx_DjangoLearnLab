from django.shortcuts import render, redirect
from .forms import Register, PostForms
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators  import login_required
from django.contrib.auth.models import User
from .models import Post


@login_required(login_url = '/login/')

def home(request):
    posts = Post.objects.all()  
    
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        print(post_id)   
        Post.objects.filter(id=post_id, author=request.user).delete()
        return redirect("home")

    return render(request, "blog/home.html", {"posts": posts})

def profile(request):
    pass   

def blog_post(request):
    if request.method == "POST":
        form = PostForms(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForms()

    return render(request, "blog/blog_post.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully")
            return redirect("login")
    else:
        form = Register()

    return render(request, "blog/register.html", {"form": form})

def logout_user(request):
    logout(request)
    return redirect("/login/")