from django.urls import include, path, re_path

from apps.facerecog.views import CitraWajahKaryawanList, CitraWajahViewset

from .views import *

citra_wajah = CitraWajahViewset.as_view({"get": "list", "post": "create"})
# citra_wajah_list = CitraWajahKaryawanList.as_view()
karyawan_me = KaryawanViewSet.as_view({"get": "me", "put": "me", "patch": "me"})

urlpatterns = [
    # path("me", karyawan_me, name="karyawan-me"),
    path("<int:karyawan_id>/citra-wajah", citra_wajah, name="karyawan-citrawajah"),
    # path(
    #     "<int:karyawan_id>/citra-wajah", citra_wajah_list, name="karyawan-citra-wajah"
    # ),
]
