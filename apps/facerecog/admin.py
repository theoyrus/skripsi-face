from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from core.helpers.db import TableExists

# Register your models here.
from .models import CitraWajah


class CitraWajahAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in CitraWajah._meta.get_fields()]
    list_display = ["citrawajah_id", "karyawan", "nama"]


admin.site.register(CitraWajah, CitraWajahAdmin)

# Permission related
if TableExists("django_content_type"):
    # hanya eksekusi jika django sudah runable
    content_type = ContentType.objects.get_for_model(CitraWajah)
    # tambah permission mengubah data citrawajah lain
    permission, created = Permission.objects.get_or_create(
        codename="change_another_citrawajah",
        name="Can change another citrawajah",
        content_type=content_type,
    )
    # tambah permission melihat data citrawajah lain
    permission, created = Permission.objects.get_or_create(
        codename="view_another_citrawajah",
        name="Can view another citrawajah",
        content_type=content_type,
    )
    # tambah permission menghapus data citrawajah lain
    permission, created = Permission.objects.get_or_create(
        codename="delete_another_citrawajah",
        name="Can delete another citrawajah",
        content_type=content_type,
    )
