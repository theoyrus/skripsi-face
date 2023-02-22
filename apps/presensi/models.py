from django.db import models

from apps.karyawan.models import Karyawan
from apps.main.models import BaseModel


# Create your models here.
class Presensi(BaseModel):
    JENIS_PRESENSI = (
        ("IN", "Datang"),
        ("OUT", "Pulang"),
    )

    presensi_id = models.BigAutoField(primary_key=True)
    karyawan = models.ForeignKey(
        Karyawan, on_delete=models.DO_NOTHING, related_name="presensi_karyawan"
    )
    tanggal = models.DateField(null=False, blank=False)
    waktu_hadir = models.DateTimeField(null=True, blank=True)
    waktu_pulang = models.DateTimeField(null=True, blank=True)
    jenis = models.CharField(max_length=10, choices=JENIS_PRESENSI)
    # catatan = models.CharField(max_length=255, null=True, blank=True)
    # latitude = models.DecimalField(
    #     max_digits=22, decimal_places=16, blank=True, null=True
    # )
    # longitude = models.DecimalField(
    #     max_digits=22, decimal_places=16, blank=True, null=True
    # )
    # foto = models.ImageField(
    #     "Foto Presensi", blank=False, null=False, upload_to="attendaces/"
    # )

    class Meta:
        db_table = "presensi"
        ordering = ["karyawan_id", "created"]
        verbose_name_plural = "presensi"

    def __str__(self):
        return f"{self.tanggal} - {self.jenis}"
