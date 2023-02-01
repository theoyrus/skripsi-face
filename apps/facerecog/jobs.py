from PIL import Image
import numpy as np
from core.settings import MEDIA_ROOT
from apps.facerecog.models import CitraWajah
from .recognizer import FacialRecognizer


def training_job():
    data = list(CitraWajah.objects.all().order_by("karyawan"))

    citra_list, label_list = [], []
    if len(data) > 0:
        for i in data:
            try:
                karyawan_id = i.karyawan.karyawan_id

                citra_nama = i.nama.name
                path_citra = f"{MEDIA_ROOT}/{citra_nama}"
                datacitra = Image.open(fp=path_citra).convert("L")

                # print({"karyawan_id": citra_nama, "citra_nama": karyawan_id})
                # append data citra
                citra_list.append(np.asarray(datacitra, "uint8"))
                label_list.append(karyawan_id)
            except Exception as e:
                print("error", e)
                pass
        # print("trained : ", label_list, "citra :", citra_list)

        recognizer = FacialRecognizer()
        recognizer.training_lbph(citra_list, np.array(label_list))
    return {"label_list": label_list}
