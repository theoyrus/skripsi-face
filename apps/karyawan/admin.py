from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from core.helpers.db import TableExists

# Register your models here.
from .models import Karyawan


class KaryawanAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Karyawan._meta.get_fields()]
    list_display = ["karyawan_id", "user", "noinduk", "nama"]


admin.site.register(Karyawan, KaryawanAdmin)


# Permission related
if TableExists("django_content_type"):
    content_type = ContentType.objects.get_for_model(Karyawan)
    # tambah permission mengubah data karyawan lain
    permission, created = Permission.objects.get_or_create(
        codename="change_another_karyawan",
        name="Can change another karyawan",
        content_type=content_type,
    )
    # tambah permission melihat data karyawan lain
    permission, created = Permission.objects.get_or_create(
        codename="view_another_karyawan",
        name="Can view another karyawan",
        content_type=content_type,
    )
    # tambah permission menghapus data karyawan lain
    permission, created = Permission.objects.get_or_create(
        codename="delete_another_karyawan",
        name="Can delete another karyawan",
        content_type=content_type,
    )
