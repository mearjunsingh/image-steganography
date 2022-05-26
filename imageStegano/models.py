import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("user"), editable=False
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
    original_image = models.ImageField(_("original image"))
    reciever_public_key = models.TextField(_("reciever public key"))
    encrypted_image = models.ImageField(_("encrypted image"), blank=True, null=True)


class Decrypt(BaseModel):
    encrypted_image = models.ImageField(_("encrypted image"))
    message = models.TextField(_("message from image"), blank=True, null=True)
