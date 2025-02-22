from datetime import datetime

import pytz
from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import User
from .permissions import IsOwnerOrAdmin
from .serializers import (TokenInfoSerializer, TokenRefreshSerializer,
                          UserLoginSerializer, UserRegisterSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            201: UserSerializer,
            400: 'Bad Request'
        },
        operation_description="Register a new user",
        security=[]
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = self.get_tokens_for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': tokens,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: UserSerializer,
            401: 'Invalid credentials'
        },
        operation_description="Login with username and password",
        security=[]
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user:
                tokens = self.get_tokens_for_user(user)
                return Response({
                    'user': UserSerializer(user).data,
                    'tokens': tokens,
                    'message': 'Login successful'
                })
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=TokenRefreshSerializer,
        responses={
            200: openapi.Response(
                description="Token refresh successful",
                examples={
                    "application/json": {
                        "access": "new_access_token",
                        "refresh": "new_refresh_token"
                    }
                }
            ),
            401: 'Invalid refresh token'
        },
        operation_description="Refresh access token using refresh token",
        security=[]
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def refresh_token(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = RefreshToken(serializer.validated_data['refresh'])
                return Response({
                    'access': str(refresh_token.access_token),
                    'refresh': str(refresh_token)
                })
            except TokenError:
                return Response(
                    {'error': 'Invalid refresh token'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=TokenInfoSerializer,
        responses={
            200: openapi.Response(
                description="Token information",
                examples={
                    "application/json": {
                        "expires_at": "2024-02-23T12:00:00Z",
                        "remaining_time": "55 minutes"
                    }
                }
            ),
            401: 'Invalid token'
        },
        operation_description="Get token expiration information",
        security=[]
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def token_info(self, request):
        serializer = TokenInfoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = AccessToken(serializer.validated_data['token'])
                exp_timestamp = token['exp']
                exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=pytz.UTC)
                now = datetime.now(pytz.UTC)
                remaining_time = exp_datetime - now

                return Response({
                    'expires_at': exp_datetime.isoformat(),
                    'remaining_time': str(remaining_time).split('.')[0],
                    'is_valid': True
                })
            except TokenError:
                return Response(
                    {'error': 'Invalid token'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
