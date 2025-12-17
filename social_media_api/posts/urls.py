from django.urls import path
from .views import PostViewSet, CommentViewSet

urlpatterns = [
    path('create-post/',PostViewSet.as_view({'get': 'list', 
                                             'put':  'update',
                                             'post': 'create'}),
         name='create-post'),
    
    path('create-post/',CommentViewSet.as_view({'get': 'list', 
                                                'put':  'update',
                                                'post': 'create'}),
         name='create-post'),
                                                      
]
