from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
from django.shortcuts import get_object_or_404
User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed_view(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

    data = PostSerializer(posts, many=True).data
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.author:
        return Response({"detail":'you cannnot like your own post'}, status=400)
    
    like, created = like.objects.get_or_create_user(user= request.user, post=post)
    if not created:
        return Response({"detail": "You already liked this post."}, status=400)

    return Response({"detail": "Post liked!"}, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])

def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
     
    like = like.objects.get_or_create_user(user= request.user, post=post)
    if not like:
        return Response({"detail":'you have not liked post'}, status=400)
    like.delete()
    return Response({"detail":'you have unliked this post'}, status=200)