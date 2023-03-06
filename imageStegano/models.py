import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from algorithm.rsa import RSA
from algorithm.steganography import ImageSteganography

from .utils import upload_path

User = get_user_model()


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        editable=False,
    )

    timestamp = models.DateTimeField(_("created on"), auto_now_add=True)

    def __str__(self):
        return self.timestamp.strftime("%A, %d %b %Y, %I:%M %p")

    def save(self, *args, **kwargs) -> None:
        if not self.id:
            self.id = uuid.uuid4()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Encrypt(BaseModel):
    message = models.TextField(_("message to hide"))
    original_image = models.ImageField(
        _("original image"),
        upload_to=upload_path,
    )
    reciever_public_key = models.TextField(_("reciever public key"))
    encrypted_image = models.ImageField(
        _("encrypted image"),
        upload_to=upload_path,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        encrypted_text = RSA.encrypt_message(
            self.reciever_public_key,
            self.message,
        )
        self.encrypted_image = ImageSteganography().encode_text_into_image(
            encrypted_text,
            self.original_image,
        )
        return super().save(*args, **kwargs)


class Decrypt(BaseModel):
    encrypted_image = models.ImageField(
        _("encrypted image"),
        upload_to=upload_path,
    )
    message = models.TextField(_("message from image"), blank=True, null=True)

    def save(self, *args, **kwargs):
        encrypted_text = ImageSteganography().decode_text_from_image(
            self.encrypted_image,
        )
        self.message = RSA.decrypt_message(
            self.user.private_key,
            encrypted_text,
        )
        return super().save(*args, **kwargs)
