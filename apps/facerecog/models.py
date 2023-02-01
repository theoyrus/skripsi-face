from django.db import models
from PIL import Image, ImageOps

from apps.karyawan.models import Karyawan
from apps.main.models import BaseModel
from core.settings import MEDIA_ROOT

from .recognizer import FacialRecognizer


# Create your models here.
class CitraWajah(BaseModel):
    citrawajah_id = models.BigAutoField(primary_key=True)
    karyawan = models.ForeignKey(
        Karyawan, on_delete=models.DO_NOTHING, related_name="citra_karyawan"
    )
    nama = models.ImageField("Citra Wajah", blank=False, null=False, upload_to="faces/")

    def save(self, *args, **kwargs):
        if self.nama:
            # Format id karyawan = 00XX
            padded_karyawan_id = str(self.karyawan.karyawan_id).rjust(4, "0")
            from datetime import datetime

            now = datetime.now().strftime("%Y%m%d%H%M%S")

            # Sesuaikan direktori wajah pada masing-masing direktori karyawan
            path_faces = f"{MEDIA_ROOT}/faces/{padded_karyawan_id}"
            import os

            if not os.path.exists(path_faces):
                os.makedirs(path_faces, exist_ok=True)

            citra = Image.open(self.nama)
            citra = ImageOps.exif_transpose(citra)
            citra_ext = self.nama.file.content_type
            citra_nama = str(f"k-{padded_karyawan_id}-{now}")
            citra_ext = citra_ext.split("/")[1]

            # setelah ditest format png lebih baik sebagai dataset daripada jpg
            # maka manfaatkan library PIL untuk mengkonversi image menjadi png

            citra_png_ext = "png"
            nama_file = f"{citra_nama}.{citra_ext}"
            nama_file_png = f"{citra_nama}.{citra_png_ext}"

            # langsung siapkan gambar menjadi citra wajah yg grayscale
            recognizer = FacialRecognizer()
            recognizer.prepare_image(citra).save(
                f"{path_faces}/{nama_file_png}", citra_png_ext
            )
            self.nama = f"faces/{padded_karyawan_id}/{nama_file_png}"

        super(CitraWajah, self).save(*args, **kwargs)

    class Meta:
        db_table = "citrawajah"
        ordering = ["karyawan_id", "created"]
        verbose_name_plural = "citra wajah"

    def __str__(self):
        return self.nama.name
