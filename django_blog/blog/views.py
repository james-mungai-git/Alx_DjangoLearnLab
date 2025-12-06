from django.shortcuts import render, redirect
from .forms import Register
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

def home(request):
    return render(request, 'blog/base.html')

def sign_up(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully")
            return redirect("login")
    else:
        form = Register()

    return render(request, "blog/sign_up.html", {"form": form})