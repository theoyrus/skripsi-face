from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend


from .filters import KaryawanFilter
from .models import Divisi, Karyawan
from .permissions import DivisiModelPermissions, KaryawanModelPermissions
from .serializers import (
    DivisiCreateSerializer,
    DivisiSerializer,
    KaryawanCitraSerializer,
    KaryawanCreateSerializer,
    KaryawanMeSerializer,
    KaryawanMeUpdateSerializer,
    KaryawanSerializer,
)


# Create your views here.
class KaryawanViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk mengelola data karyawan
    """

    queryset = Karyawan.objects.all()
    serializer_class = KaryawanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = KaryawanFilter
    # serializer_class = KaryawanCitraSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            # jika proses create/update, pakai serializer yg berbeda
            return KaryawanCreateSerializer
        elif self.action in ("me", "saya"):
            if self.request.method in ["PUT"]:
                return KaryawanMeUpdateSerializer
            return KaryawanMeSerializer
        elif self.action in ["list"]:
            # jika proses list, pakai serializer non permission
            return KaryawanSerializer
        return KaryawanSerializer

    def get_permissions(self):
        if self.action in ("me", "saya"):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, KaryawanModelPermissions]
        return [permission() for permission in permission_classes]

    def get_object(self):
        from django.core.exceptions import ObjectDoesNotExist

        if self.action in ("me"):
            try:
                return self.queryset.get(user=self.request.user)
            except ObjectDoesNotExist:
                from core.helpers.exception_api import KaryawanUserError

                raise KaryawanUserError("Sesi karyawan belum diatur")
        return super().get_object()

    # custom action
    @action(["get", "put"], detail=False)
    def me(self, request, *args, **kwargs):
        """
        API endpoint Karyawan sesuai sesi
        """
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)


class DivisiViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk mengelola data divisi
    """

    queryset = Divisi.objects.all()
    # serializer_class = DivisiSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return DivisiCreateSerializer
        return DivisiSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated, DivisiModelPermissions]
        return [permission() for permission in permission_classes]
