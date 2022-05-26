from django import forms

from .models import Decrypt, Encrypt


class EncryptFrom(forms.ModelForm):
    class Meta:
        model = Encrypt
        fields = ("message", "original_image", "reciever_public_key")


class DecryptForm(forms.ModelForm):
    class Meta:
        model = Decrypt
        fields = ["encrypted_image"]
