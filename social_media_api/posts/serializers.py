from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import authenticate


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "created_at"]
        read_only_fields = ["id", "author", "created_at"] 
        
    def create(self, validated_data):
        post = Post.objects.create(
            author = validated_data["author"],
            title=validated_data["title"],
            content=validated_data["content"],
        )
        return post

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["author","content"]
        
        def create(self,validated_data):
            comment=comment.objects.create(
                author = validated_data["author"],
                content=validated_data.get("content","")
            )
            
            return comment
        