from rest_framework import serializers
from .models import BlogPost, Comment, Like
from users.serializers import ProfileSerializer

class BlogSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = "__all__"

    def get_author_name(self, obj):
        return obj.author.username if obj.author else "Anonymous"

class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(source="author.profile", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "created_at"]


class BlogPostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(source="author.profile", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ["id", "title", "content", "summary", "created_at", "author", "comments", "likes_count", "is_liked"]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False
