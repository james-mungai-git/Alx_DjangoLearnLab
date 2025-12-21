from django.urls import path
from . import views
from .views import PostViewSet, CommentViewSet, follow_user, unfollow_user, feed_view

urlpatterns = [
    path('/create-post/',PostViewSet.as_view({'get': 'list', 
                                             'put':  'update',
                                             'post': 'create'}),
         name='create-post'),
    
    path('/post-comment/',CommentViewSet.as_view({'get': 'list', 
                                                'put':  'update',
                                                'post': 'create'}),
         name='create-post'),
    path('/follow/<int:user_id>/', views.follow_user, name='follow-user'),
    path('/unfollow/<int:user_id>/',  views.unfollow_user, name='unfollow-user'),
    path('/feed/', views.feed_view, name='feed'),
                                                      
]
