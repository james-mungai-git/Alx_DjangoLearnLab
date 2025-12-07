from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path("logout/", views.logout_user, name="logout"),
    path('register/', views.register, name='register'),
    path('blog_post/', views.blog_post, name = 'blog')
]