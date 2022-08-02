from django.contrib import admin

from algorithm.rsa import RSA
from algorithm.steganography import ImageSteganography

from .forms import DecryptForm, EncryptFrom
from .models import Decrypt, Encrypt


class BaseModelAdmin(admin.ModelAdmin):
    ordering = ["-timestamp"]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(user=request.user)

    def has_add_permission(self, *args, **kwargs):
        return True

    def has_view_permission(self, *args, **kwargs):
        return True

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return True

    def has_module_permission(self, *args, **kwargs):
        return True


@admin.register(Encrypt)
class EncryptAdmin(BaseModelAdmin):
    def change_view(self, *args, **kwargs):
        self.fields = [
            ("message",),
            ("original_image",),
            ("reciever_public_key",),
            ("encrypted_image",),
        ]
        return super().change_view(*args, **kwargs)

    def add_view(self, *args, **kwargs):
        self.fields = []
        self.form = EncryptFrom
        return super().add_view(*args, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        encrypted_text = RSA().encrypt_message(obj.reciever_public_key, obj.message)
        obj.encrypted_image = ImageSteganography().encode_text_into_image(
            encrypted_text, obj.original_image
        )
        obj.save()


@admin.register(Decrypt)
class DecryptAdmin(BaseModelAdmin):
    def change_view(self, *args, **kwargs):
        self.fields = [("encrypted_image",), ("message",)]
        return super().change_view(*args, **kwargs)

    def add_view(self, *args, **kwargs):
        self.fields = []
        self.form = DecryptForm
        return super().add_view(*args, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        encrypted_text = ImageSteganography().decode_text_from_image(
            obj.encrypted_image
        )
        obj.message = RSA().decrypt_message(request.user.private_key, encrypted_text)
        obj.save()
