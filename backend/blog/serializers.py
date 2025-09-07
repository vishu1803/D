from rest_framework import serializers
from .models import BlogPost, Comment, Like
from users.models import Profile  # Safe import, avoids circular import


# 🔹 Lightweight profile serializer
class AuthorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ["username", "email", "bio", "avatar"]
        read_only_fields = ["username", "email", "avatar"]


# 🔹 Blog serializer
class BlogSerializer(serializers.ModelSerializer):
    author = AuthorProfileSerializer(source="author.profile", read_only=True)
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = "__all__"
        read_only_fields = ["author"]

    def get_author_name(self, obj):
        return obj.author.username if obj.author else "Anonymous"


# 🔹 Comment serializer
class CommentSerializer(serializers.ModelSerializer):
    author = AuthorProfileSerializer(source="author.profile", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "created_at"]


# 🔹 Detailed BlogPost serializer
class BlogPostSerializer(serializers.ModelSerializer):
    author = AuthorProfileSerializer(source="author.profile", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            "id", "title", "content", "summary",
            "created_at", "author", "comments",
            "likes_count", "is_liked"
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
