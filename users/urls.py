"""
URLs for autho app of the project.
"""
from django.urls import path

from users.api import (
    TokenObtainPairAPIView,
    TokenRefreshAPIView,
    SignUpUserAPIView,
    GetCurrentUserAPIView,
    ChangePasswordAPIView,
)


urlpatterns = [
    path("signup/", SignUpUserAPIView.as_view(), name="signup"),
    path("token/", TokenObtainPairAPIView.as_view(), name="token_obtain_pair"),
    path(
        "token/refresh/",
        TokenRefreshAPIView.as_view(),
        name="token_refresh",
    ),
    path(
        "change-password/",
        ChangePasswordAPIView.as_view(),
        name="change_password",
    ),
    path("", GetCurrentUserAPIView.as_view(), name="get_current_user"),
]
