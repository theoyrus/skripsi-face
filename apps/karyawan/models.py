from django.contrib.auth import get_user_model
from django.db import models

from apps.main.models import BaseModel


# Create your models here.
class Divisi(BaseModel):
    divisi_id = models.AutoField(primary_key=True)
    kode = models.CharField(max_length=15)
    nama = models.CharField(max_length=100)

    class Meta:
        db_table = "divisi"
        verbose_name_plural = "divisi"

    def __str__(self):
        return self.nama


class Karyawan(BaseModel):
    karyawan_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="user_karyawan",
    )
    divisi = models.ForeignKey(
        Divisi,
        on_delete=models.DO_NOTHING,
        related_name="karyawan_divisi",
        blank=True,
        null=True,
    )
    noinduk = models.CharField(max_length=20)
    nama = models.CharField(max_length=150)

    class Meta:
        db_table = "karyawan"
        ordering = ["nama"]
        verbose_name_plural = "karyawan"

    def __str__(self):
        return self.nama
