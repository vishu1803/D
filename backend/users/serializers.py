from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    avatar = serializers.SerializerMethodField()  # ✅ dynamic avatar

    class Meta:
        model = Profile
        fields = ["username", "email", "bio", "avatar"]

    def get_avatar(self, obj):
        """
        If user has uploaded avatar → return that.
        Else if Google avatar exists in obj.avatar (string URL) → return that.
        """
        if obj.avatar:
            try:
                return obj.avatar.url  # FileField/ ImageField upload
            except Exception:
                return str(obj.avatar)  # If already a URL (from Google)
        return None
