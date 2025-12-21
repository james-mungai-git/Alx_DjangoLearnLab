from django.urls import path
from . import views
from .views import PostViewSet, CommentViewSet, feed_view, like_post,unlike_post

urlpatterns = [
    path('create-post/',PostViewSet.as_view({'get': 'list', 
                                             'put':  'update',
                                             'post': 'create',}),
         name='create-post'),
    path('delete-post/<int:pk>/', PostViewSet.as_view({'delete':'destroy'}), name='delete-post'),
    
    path('post-comment/',CommentViewSet.as_view({'get': 'list', 
                                                'put':  'update',
                                                'post': 'create'}),
         name='create-post'),
    path('delete-comment/<int:pk>/', CommentViewSet.as_view({'delete':'destroy'}), name='delete-comment'),

    path('feed/', views.feed_view, name='feed'),
    path('like/<int:post_id>/',views.like_post, name='like-post'),
    path('unlike/<int:post_id>/', views.unlike_post, name='unlike-post'),
                                                      
]
