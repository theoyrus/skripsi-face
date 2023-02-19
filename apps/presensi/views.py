from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    Presensi,
    KehadiranSerializer,
    KehadiranRekamSerializer,
)
from .permissions import PresensiKehadiranPermission
from .filters import KehadiranFilter


# Create your views here.
class KehadiranViewSet(ModelViewSet):
    """
    API endpoint untuk mengelola kehadiran
    """

    # parser_classes = (FileUploadParser,)
    serializer_class = KehadiranSerializer
    queryset = Presensi.objects.all()
    permission_classes = [permissions.IsAuthenticated, PresensiKehadiranPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = KehadiranFilter

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return KehadiranRekamSerializer
        return self.serializer_class

    def get_queryset(self):
        try:
            user = self.request.user
            if user.has_perm("presensi.view_another_presensi"):
                # jika punya hak view semua presensi
                if "karyawan_id" in self.kwargs:
                    # tapi jika ada path param berisi karyawan_id, filter presensi milik karyawan tersebut
                    karyawan_id = self.kwargs["karyawan_id"]
                else:
                    # jika tidak ada path param, ambil seluruh data presensi
                    return Presensi.objects.all()
            else:
                # jika tidak punya hak view semua data presensi, filter by sesi karyawan
                karyawan_id = user.user_karyawan.karyawan_id

            return Presensi.objects.filter(karyawan_id=karyawan_id)
        except ObjectDoesNotExist:
            from core.helpers.exception_api import KaryawanUserError

            raise KaryawanUserError("Sesi karyawan belum diatur")
