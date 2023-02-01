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
    waktu_hadir = models.TimeField(null=True, blank=True)
    waktu_pulang = models.TimeField(null=True, blank=True)
    jenis = models.CharField(max_length=10, choices=JENIS_PRESENSI)

    class Meta:
        db_table = "presensi"
        ordering = ["karyawan_id", "created"]
        verbose_name_plural = "presensi"

    def __str__(self):
        return f"{self.tanggal} - {self.jenis}"
