from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    profile,
    register,
    logout_user, 
    CommentListView,
    CommentDetailView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)
from django.contrib.auth.views import LoginView
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', PostListView.as_view(), name='home'),                
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), 
    path('post/new/', PostCreateView.as_view(), name='post-create'),      
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),  
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), 
    
    path('comment/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'), 
    path('post/<int:pk>/comment/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),  
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'), 

    path('profile/', profile, name='profile'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    
    
]
