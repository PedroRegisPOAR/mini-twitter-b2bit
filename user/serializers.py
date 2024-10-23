from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "name", "password"]
        # extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = User(**validated_data)
        # user.set_password(validated_data['password'])

        # Adding the below line made it work for me.
        instance.is_active = True
        if password is not None:
            # Set password does the hash, so you don't need to call make_password
            instance.set_password(password)
        instance.save()
        return instance


class FollowerSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(read_only=True, source="follower.username")
    name = serializers.CharField(read_only=True, source="follower.name")
