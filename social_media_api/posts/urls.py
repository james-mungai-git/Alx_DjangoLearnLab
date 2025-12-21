from django.urls import path
from . import views
from .views import PostViewSet, CommentViewSet, feed_view

urlpatterns = [
    path('/create-post/',PostViewSet.as_view({'get': 'list', 
                                             'put':  'update',
                                             'post': 'create'}),
         name='create-post'),
    
    path('/post-comment/',CommentViewSet.as_view({'get': 'list', 
                                                'put':  'update',
                                                'post': 'create'}),
         name='create-post'),
    path('/feed/', views.feed_view, name='feed'),
                                                      
]
