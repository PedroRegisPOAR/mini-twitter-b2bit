from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(read_only=True, source="user.username")
    user_name = serializers.CharField(read_only=True, source="user.name")

    class Meta:
        model = Post
        fields = ["id", "user_username", "user_name", "text"]


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["text"]
