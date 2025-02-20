from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "name", "password"]
        # extra_kwargs = {"password": {"write_only": True}}


class FollowerSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(read_only=True, source="follower.username")
    name = serializers.CharField(read_only=True, source="follower.name")
