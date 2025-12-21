from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author_name =serializers.SerializerMethodField(source='author')
    class Meta:
        model = Post
        fields = ["id", "author_name", "title", "content", "created_at"]
        read_only_fields = ["id", "author", "created_at"] 
        
    def create(self, validated_data):
        post = Post.objects.create(
            author = validated_data["author"],
            title=validated_data["title"],
            content=validated_data["content"],
        )
        return post
    def get_author_name(self,obj):
        return obj.author.username

class CommentSerializer(serializers.ModelSerializer):
    author_name =serializers.SerializerMethodField(source='author')

    class Meta:
        model = Comment
        fields = ["author","content"]
        
        def create(self,validated_data):
            comment=comment.objects.create(
                author = validated_data["author"],
                content=validated_data.get("content","")
            )
            
            return comment
        def get_author_name(self, obj):
            return obj.author.username