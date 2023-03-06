"""
User serializers for autho app
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class TokenObtainSerializer(TokenObtainPairSerializer):
    """
    Token Obtain serializer for autho app.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token


class SignUpUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model used in sign up.
    """

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that email already exists.",
            ),
        ],
        label="Email",
        style={"input_type": "email"},
        help_text="Enter a valid email address.",
    )
    password2 = serializers.CharField(
        validators=[validate_password],
        label="Confirm password",
        style={"input_type": "password"},
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        """
        Meta class for the serializer
        """

        model = User
        fields = ("email", "username", "password", "password2")

    def validate(self, attrs):
        """
        Check that the two password fields match.
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."},
            )
        return attrs

    def create(self, validated_data):
        """
        Create a new user with encrypted password and return it.
        """
        del validated_data["password2"]
        return User.objects.create_user(**validated_data)

    def to_representation(self, instance):
        """
        Return the JWT token to the user on successful sign up.
        """
        refresh = RefreshToken.for_user(instance)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class UserDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    public_key = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "public_key")


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model used in change password.
    """

    old_password = serializers.CharField(
        required=True,
        label="Old password",
        style={"input_type": "password"},
        help_text="Enter your old password.",
    )
    new_password = serializers.CharField(
        validators=[validate_password],
        required=True,
        label="New password",
        style={"input_type": "password"},
        help_text="Enter a new password.",
    )
    new_password2 = serializers.CharField(
        validators=[validate_password],
        required=True,
        label="Confirm new password",
        style={"input_type": "password"},
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        """
        Meta class for the serializer
        """

        model = User
        fields = ("old_password", "new_password", "new_password2")

    def validate(self, attrs):
        """
        Check that the two password fields match.
        """
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."},
            )
        return attrs

    def update(self, instance, validated_data):
        """
        Update the password of the user.
        """
        old_password = validated_data.get("old_password")
        new_password = validated_data.get("new_password")
        if instance.check_password(old_password):
            instance.set_password(new_password)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(
                {"old_password": "Old password is incorrect."},
            )

    def to_representation(self, instance):
        """
        Return the JWT token to the user on successful sign up.
        """
        refresh = RefreshToken.for_user(instance)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
