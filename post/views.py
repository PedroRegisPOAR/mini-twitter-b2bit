from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Post
from .serializers import CreatePostSerializer, PostSerializer




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
