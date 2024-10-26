from rest_framework import serializers
from .models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(read_only=True, source="user.username")
    user_name = serializers.CharField(read_only=True, source="user.name")

    class Meta:
        model = Post
        fields = ["id", "user_username", "user_name", "text", "image"]


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["text", "image"]


class CreateLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id"]
