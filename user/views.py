from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User, Follower
from .serializers import UserSerializer, FollowerSerializer
from .pagination import CustomPagination


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class UserViewSet(ViewSet):
    # permission_classes = [IsAuthenticated]

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

    @extend_schema(responses={204: FollowerSerializer})
    @action(detail=True)
    def follow(self, request, pk=None):
        try:
            to_follow = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado!'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        Follower.objects.create(following=to_follow, follower=user)

        return Response(status=status.HTTP_204_NO_CONTENT)
