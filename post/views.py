from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated

from user.models import User
from .models import Post, Like
from .serializers import CreatePostSerializer, PostSerializer, CreateLikeSerializer




class PostViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=CreatePostSerializer, responses={201: PostSerializer})
    def create(self, request):
        data = request.data
        user = request.user

        serializer = CreatePostSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        post = Post.objects.create(user=user, **validated_data)

        serializer = PostSerializer(instance=post)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(responses={204: PostSerializer})
    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        try:
            Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post não encontrado!'}, status=status.HTTP_404_NOT_FOUND)

        try:
            post = Post.objects.get(pk=pk)
            post.delete()
        except Post.DoesNotExist:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses={201: PostSerializer})
    @action(detail=True, methods=['patch'])
    def edit(self, request, pk=None):
        try:
            Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post não encontrado!'}, status=status.HTTP_404_NOT_FOUND)

        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        post.text = validated_data["text"]
        post.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


    @extend_schema(responses={201: PostSerializer})
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Post não encontrado!'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        # Actually creates the like
        Like.objects.create(user=user, post=post)

        return Response(status=status.HTTP_201_CREATED)

# TODO:
class LikeViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={201: CreateLikeSerializer})
    def create(self, request):
        data = request.data
        user = request.user

        serializer = CreateLikeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        Like.objects.create(user=user, **validated_data)

        return Response(status=status.HTTP_201_CREATED)
