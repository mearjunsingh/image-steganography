from .base import *

DEBUG = False

ALLOWED_HOSTS = ["example.com"]

STATIC_URL = "static/"
STATIC_ROOT = "static_CDN"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
MEDIA_ROOT = "uploads"
