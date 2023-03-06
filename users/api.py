"""
User API views for autho app.
"""

from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.serializers import (
    SignUpUserSerializer,
    TokenObtainSerializer,
    UserDetailSerializer,
    ChangePasswordSerializer,
)


User = get_user_model()


class SignUpUserAPIView(CreateAPIView):
    """
    Register a new user in the system.
    """

    permission_classes = (AllowAny,)
    serializer_class = SignUpUserSerializer


class TokenObtainPairAPIView(TokenObtainPairView):
    """
    Get JWT token for user authentication and authorization
    purpose in the system. This token will be used in the
    header of the request.
    """

    permission_classes = (AllowAny,)
    serializer_class = TokenObtainSerializer


class TokenRefreshAPIView(TokenRefreshView):
    """
    Refresh JWT token for user authentication and
    authorization purpose in the system.
    """

    pass


class GetCurrentUserAPIView(APIView):
    """
    Get current user details.
    """

    def get(self, request):
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = UserDetailSerializer(
            user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ChangePasswordAPIView(APIView):
    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        return Response({"detail": "Password has been changed."})
