from django.contrib import admin
from django.utils.safestring import mark_safe

from .forms import DecryptForm, EncryptFrom
from .models import Decrypt, Encrypt


@admin.register(Encrypt)
class EncryptAdmin(admin.ModelAdmin):
    list_display = [
        "thumbnail",
        "user",
        "timestamp",
        "id",
    ]
    rf = readonly_fields = [
        "id",
        "user",
        "timestamp",
        "_original_image",
        "_encrypted_image",
    ]
    search_fields = ["message", "reciever_public_key", "user__username", "id"]
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]
    list_select_related = ["user"]
    fs = fieldsets = (
        (
            None,
            {
                "fields": ("_encrypted_image",),
            },
        ),
        (
            "Source Data",
            {
                "fields": (
                    "message",
                    "_original_image",
                    "reciever_public_key",
                ),
            },
        ),
        (
            "Meta",
            {
                "classes": ("collapse",),
                "fields": (
                    "id",
                    "user",
                    "timestamp",
                ),
            },
        ),
    )

    def change_view(self, *args, **kwargs):
        self.fieldsets = self.fs
        self.readonly_fields = self.rf
        return super().change_view(*args, **kwargs)

    def add_view(self, *args, **kwargs):
        self.fieldsets = []
        self.readonly_fields = []
        self.form = EncryptFrom
        return super().add_view(*args, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def thumbnail(self, obj):
        img_url = obj.original_image.url
        img_tag = f'<img src="{img_url}" width="100" height="100"/>'
        return mark_safe(img_tag)

    def _original_image(self, obj):
        img_url = obj.original_image.url
        img_tag = f'<img src="{img_url}" width="300" height="300"/>'
        return mark_safe(img_tag)

    def _encrypted_image(self, obj):
        img_url = obj.encrypted_image.url
        img_tag = f'<img src="{img_url}" width="500" height="500"/>'
        return mark_safe(img_tag)

    def has_change_permission(self, *args, **kwargs):
        return False


@admin.register(Decrypt)
class DecryptAdmin(admin.ModelAdmin):
    list_display = ["thumbnail", "user", "timestamp", "id"]
    rf = readonly_fields = ["id", "user", "timestamp", "_encrypted_image"]
    search_fields = ["message", "user__username", "id"]
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]
    list_select_related = ["user"]
    fs = fieldsets = (
        (
            None,
            {
                "fields": ("message",),
            },
        ),
        (
            "Source Data",
            {
                "fields": ("_encrypted_image",),
            },
        ),
        (
            "Meta",
            {
                "classes": ("collapse",),
                "fields": (
                    "id",
                    "user",
                    "timestamp",
                ),
            },
        ),
    )

    def change_view(self, *args, **kwargs):
        self.fieldsets = self.fs
        self.readonly_fields = self.rf
        return super().change_view(*args, **kwargs)

    def add_view(self, *args, **kwargs):
        self.fieldsets = []
        self.readonly_fields = []
        self.form = DecryptForm
        return super().add_view(*args, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def thumbnail(self, obj):
        img_url = obj.encrypted_image.url
        img_tag = f'<img src="{img_url}" width="100" height="100"/>'
        return mark_safe(img_tag)

    def _encrypted_image(self, obj):
        img_url = obj.encrypted_image.url
        img_tag = f'<img src="{img_url}" width="300" height="300"/>'
        return mark_safe(img_tag)

    def has_change_permission(self, *args, **kwargs):
        return False
