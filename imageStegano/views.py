from rest_framework.response import Response
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from algorithm.steganography import ImageSteganographyException

from .models import Encrypt, Decrypt
from .serializers import EncryptSerializer, DencryptSerializer


class BaseViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class EncryptViewSet(BaseViewSet):
    queryset = Encrypt.objects.all()
    serializer_class = EncryptSerializer


class DencryptViewSet(BaseViewSet):
    queryset = Decrypt.objects.all()
    serializer_class = DencryptSerializer

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
        except ImageSteganographyException as e:
            response = Response({"detail": str(e)}, status=400)

        return response
