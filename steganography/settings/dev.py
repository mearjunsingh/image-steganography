from .base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

STATIC_URL = "static/"
STATIC_ROOT = "static_CDN"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
MEDIA_ROOT = "uploads"
