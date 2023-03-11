from django.urls import path

from rest_framework.routers import DefaultRouter

from .api import EncryptViewSet, DencryptViewSet
from .views import HomePageView

router = DefaultRouter()

router.register("encrypt", EncryptViewSet, basename="encrypt")
router.register("decrypt", DencryptViewSet, basename="dencrypt")

urlpatterns = [
    path("", HomePageView.as_view(), name="home-page-view"),
]

urlpatterns += router.urls
