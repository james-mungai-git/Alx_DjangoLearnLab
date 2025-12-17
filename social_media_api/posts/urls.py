from django.urls import path
from .views import PostViewSet, CommentViewSet

urlpatterns = [
    path('api/create-post/',PostViewSet.as_view({'get': 'list', 
                                             'put':  'update',
                                             'post': 'create'}),
         name='create-post'),
    
    path('api/post-comment/',CommentViewSet.as_view({'get': 'list', 
                                                'put':  'update',
                                                'post': 'create'}),
         name='create-post'),
                                                      
]
