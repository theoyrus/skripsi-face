from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from core.helpers.db import TableExists

# Register your models here.
from .models import Presensi


class KehadiranAdmin(admin.ModelAdmin):
    list_display = (
        "presensi_id",
        "karyawan",
        "jenis",
        "tanggal",
        "waktu_hadir",
        "waktu_pulang",
    )
    list_filter = ("karyawan__divisi", "karyawan", "tanggal")


admin.site.register(Presensi, KehadiranAdmin)

# permission related
if TableExists("django_content_type"):
    # hanya eksekusi jika django sudah runable
    content_type = ContentType.objects.get_for_model(Presensi)
    # tambah permission menambah presensi user lain
    permission, created = Permission.objects.get_or_create(
        codename="view_another_presensi",
        name="Can view another presensi",
        content_type=content_type,
    )
    # tambah permission menambah presensi user lain
    permission, created = Permission.objects.get_or_create(
        codename="add_another_presensi",
        name="Can add another presensi",
        content_type=content_type,
    )
    # tambah permission mengubah presensi user lain
    permission, created = Permission.objects.get_or_create(
        codename="change_another_presensi",
        name="Can change another presensi",
        content_type=content_type,
    )
    # tambah permission menghapus presensi user lain
    permission, created = Permission.objects.get_or_create(
        codename="delete_another_presensi",
        name="Can delete another presensi",
        content_type=content_type,
    )
