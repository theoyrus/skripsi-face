from apps import karyawan
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    Presensi,
    KehadiranSerializer,
    KehadiranRekamSerializer,
    KehadiranHariIniSerializer,
    KehadiranBulanIniSerializer,
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
        elif self.action in ("hariini"):
            return KehadiranHariIniSerializer
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

    def get_permissions(self):
        if self.action in ["hariini", "bulanini"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [
                permissions.IsAuthenticated,
                PresensiKehadiranPermission,
            ]
        return [permission() for permission in permission_classes]

    def get_object(self):
        from django.core.exceptions import ObjectDoesNotExist

        if self.action in ["hariini"]:
            try:
                tanggal = timezone.now().date()
                tanggal_gmt7 = (
                    timezone.now()
                    .astimezone(timezone.pytz.timezone("Asia/Jakarta"))
                    .date()
                )
                return self.queryset.get(
                    karyawan=self.request.user.user_karyawan.karyawan_id,
                    tanggal=tanggal_gmt7,
                )
            except ObjectDoesNotExist:
                raise NotFound(detail="Belum ada rekaman presensi hari ini")
        return super().get_object()

    # custom action
    @action(["get"], detail=False)
    def hariini(self, request, *args, **kwargs):
        """
        API endpoint kehadiran hari ini
        """
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)

    @action(["get"], detail=False)
    def bulanini(self, request, *args, **kwargs):
        """
        API endpoint kehadiran bulan ini
        """
        if request.method == "GET":
            sql = """
            select presensi_id
            ,karyawan_id
            ,sum(if(waktu_hadir is not null,1,0)) as hadir
            ,sum(if(TIME(waktu_hadir) > TIME('01:00:00'),1,0)) as terlambat
            ,sum(if(waktu_hadir is null,1,0)) as tidak_hadir
            from presensi
            where karyawan_id=%(kry_id)s
            and month(tanggal)=MONTH(now())
            and year(tanggal)=YEAR(NOW())
            -- GROUP BY karyawan_id
            """
            params = {"kry_id": request.user.user_karyawan.karyawan_id}
            qs = Presensi.objects.raw(sql, params)
            serializer = KehadiranBulanIniSerializer(qs, many=True)
            return Response({"data": serializer.data[0]})
