from rest_framework.routers import DefaultRouter

from .views import EncryptViewSet, DencryptViewSet

router = DefaultRouter()

router.register("encrypt", EncryptViewSet, basename="encrypt")
router.register("decrypt", DencryptViewSet, basename="dencrypt")

urlpatterns = router.urls
