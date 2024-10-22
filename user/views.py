from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from .models import User, Follower
from .serializers import UserSerializer, FollowerSerializer
from .pagination import CustomPagination


class UserViewSet(ViewSet):
    @extend_schema(request=UserSerializer, responses={201: UserSerializer})
    def create(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = User.objects.create(**validated_data)
        serializer = UserSerializer(instance=user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(responses={200: FollowerSerializer})
    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado!'}, status=status.HTTP_404_NOT_FOUND)

        paginator = CustomPagination()
        followers = Follower.objects.filter(following=user)
        page = paginator.paginate_queryset(followers, request)

        if page is not None:
            serializer = FollowerSerializer(instance=followers, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = FollowerSerializer(instance=followers, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
