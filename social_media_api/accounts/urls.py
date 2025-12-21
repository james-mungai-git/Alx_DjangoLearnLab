from django.urls import path, include
from .views import RegisterView, LoginView, ProfileView, follow_user, unfollow_user
from . import views

urlpatterns = [
    path('/register/', RegisterView.as_view(),name="register"),
    path('/login/', LoginView.as_view(), name="login"),
    path('/profile/', ProfileView.as_view(), name="profile"),
    path('/follow/<int:user_id>/', views.follow_user, name='follow-user'),
    path('/unfollow/<int:user_id>/',  views.unfollow_user, name='unfollow-user'),
    
]