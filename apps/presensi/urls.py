from django.urls import include, re_path
from apps.presensi.views import KehadiranViewSet
from core.helpers.router import OptionalSlashRouter


router = OptionalSlashRouter()
router.register("kehadiran", KehadiranViewSet, basename="presensi")

urlpatterns = [
    # re_path(r"", index, name="index"),
    re_path(r"", include(router.urls)),
]
