from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
import pytz, datetime

from apps.main.serializers import BaseHyperlinkedModelSerializer
from .models import Presensi
from apps.karyawan.serializers import KaryawanSerializer
from core.helpers.preferensi import get_userpref_timezone


class KehadiranSerializer(BaseHyperlinkedModelSerializer):
    # karyawan_nama = serializers.ReadOnlyField(source="karyawan.nama")
    karyawan = KaryawanSerializer(context={"is_data": False})

    class Meta:
        model = Presensi
        # fields = "__all__"
        fields = (
            "url",
            "presensi_id",
            "karyawan",
            "tanggal",
            "waktu_hadir",
            "waktu_pulang",
            "created",
            "updated",
        )

    def to_representation(self, instance):
        self.fields["waktu_hadir"] = serializers.DateTimeField(
            default_timezone=get_userpref_timezone(self)
        )
        self.fields["waktu_pulang"] = serializers.DateTimeField(
            default_timezone=get_userpref_timezone(self)
        )
        return super().to_representation(instance)


class KehadiranRekamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presensi
        fields = ["karyawan", "jenis", "waktu_hadir", "waktu_pulang"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get("request").user
        if user.has_perm("presensi.add_another_presensi") or user.is_superuser:
            self.fields["karyawan"].required = True
        elif user.has_perm("presensi.change_presensi") or user.is_superuser:
            pass
        else:
            self.fields.pop("karyawan")
            self.fields.pop("waktu_hadir")
            self.fields.pop("waktu_pulang")

    def create(self, validated_data):
        data = validated_data
        request = self.context["request"]
        user = request.user

        if user.has_perm("presensi.add_another_presensi") or user.is_superuser:
            data["karyawan_id"] = self.initial_data["karyawan"]
        else:
            # jika tidak punya hak, kunci sesi karyawan
            try:
                data["karyawan_id"] = request.user.user_karyawan.karyawan_id
            except ObjectDoesNotExist:
                from core.helpers.exception_api import KaryawanUserError

                raise KaryawanUserError("Sesi karyawan belum diatur")

        karyawan = data["karyawan_id"]
        jenis = data["jenis"]
        tanggal = timezone.now().date()
        data["tanggal"] = tanggal

        # Cek apakah presensi sudah ada untuk karyawan dan tanggal saat ini
        try:
            presensi = Presensi.objects.get(karyawan=karyawan, tanggal=tanggal)
        except Presensi.DoesNotExist:
            presensi = None

        # jika belum ada presensi, rekam data baru
        if not presensi:
            if jenis == "IN":
                data["waktu_hadir"] = timezone.now().replace(microsecond=0)
                return super().create(data)
            else:
                raise serializers.ValidationError("Presensi IN belum ada")

        # jika sudah ada presensi, update presensi
        else:
            if jenis == "OUT":
                if presensi.waktu_pulang is not None:
                    raise serializers.ValidationError("Presensi OUT sudah terekam")

                presensi.waktu_pulang = timezone.now().replace(microsecond=0)
                presensi.save()
                return presensi
            else:
                raise serializers.ValidationError("Presensi IN sudah terekam")

    def update(self, instance, validated_data):
        waktu_hadir = validated_data.get("waktu_hadir")
        waktu_pulang = validated_data.get("waktu_pulang")

        print(f"waktu_hadir: {waktu_hadir}")

        # Anggap timezone dari client/user Asia/Jakarta
        # timezone_user = pytz.timezone("Asia/Jakarta")
        timezone_user = get_userpref_timezone()

        if waktu_hadir:
            waktu_hadir_tz = timezone_user.localize(waktu_hadir.replace(tzinfo=None))
            # Ubah timezone menjadi UTC
            waktu_hadir_utc = waktu_hadir_tz.astimezone(pytz.utc)
            validated_data["waktu_hadir"] = waktu_hadir_utc

        if waktu_pulang:
            waktu_pulang_tz = timezone_user.localize(waktu_pulang.replace(tzinfo=None))
            # Ubah timezone menjadi UTC
            waktu_pulang_utc = waktu_pulang_tz.astimezone(pytz.utc)
            validated_data["waktu_pulang"] = waktu_pulang_utc

        return super().update(instance, validated_data)
