from rest_framework import serializers

from .models import Encrypt, Decrypt


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = self.context["request"].user
        return data


class EncryptSerializer(BaseSerializer):
    message = serializers.CharField()
    original_image = serializers.ImageField()
    reciever_public_key = serializers.CharField()
    encrypted_image = serializers.ImageField(read_only=True)

    class Meta:
        model = Encrypt
        fields = [
            "id",
            "message",
            "original_image",
            "reciever_public_key",
            "encrypted_image",
        ]


class DencryptSerializer(BaseSerializer):
    encrypted_image = serializers.ImageField()
    message = serializers.CharField(read_only=True)

    class Meta:
        model = Decrypt
        fields = ["id", "encrypted_image", "message"]
