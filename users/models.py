import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from algorithm.rsa import RSA


class User(AbstractUser):
    id = models.UUIDField(_("user id"), primary_key=True, editable=False)
    public_key = models.TextField(_("public key"), blank=True, null=True)
    private_key = models.TextField(_("private key"), blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        if not self.public_key or not self.private_key:
            self.public_key, self.private_key = RSA().generate_keys()
        self.is_staff = True
        return super().save(*args, **kwargs)
