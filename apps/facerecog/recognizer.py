import cv2 as ocv
import numpy as np
from PIL import Image

from core.settings import ASSETS_ROOT

from rest_framework.exceptions import APIException


class RecognizerError(APIException):
    status_code = 400
    default_code = "bad_request"
    pass


class FacialRecognizer:
    def __init__(self, classifier_path="classifier-LBPH.yml"):
        self.classifier = ocv.face.LBPHFaceRecognizer_create()
        self.classifier_path = f"{ASSETS_ROOT}/{classifier_path}"

    def prepare_image_old(self, img):
        # menyiapkan citra yg diinput hanya citra grayscale & terdapat wajah
        img = img.convert("L")
        citra = np.asarray(img, "uint8")
        wajah = self.extract_wajah(citra)
        if len(wajah) > 0:
            return Image.fromarray(wajah)
        else:
            raise RecognizerError("Tidak ada wajah terdeteksi")

    def prepare_image(self, img):
        # Load gambar dan konversi ke numpy array
        img = np.asarray(img.convert("L"), dtype=np.uint8)

        # Ekstraksi wajah
        wajah = self.extract_wajah(img)

        # Cek apakah berhasil ekstraksi wajah
        if len(wajah) == 0:
            raise RecognizerError("Tidak ada wajah terdeteksi")

        # Konversi kembali ke PIL Image
        return Image.fromarray(wajah)

    def extract_wajah(self, img):
        classifier_wajah = ocv.CascadeClassifier(
            f"{ASSETS_ROOT}/haarcascade_frontalface_default.xml"
        )
        wajah = classifier_wajah.detectMultiScale(img)
        px = 150
        if len(wajah) > 0:
            x = wajah[0][0]
            y = wajah[0][1]
            lar = wajah[0][2]
            alt = wajah[0][3]
            wajah = img[y : y + lar, x : x + alt]
            wajah = ocv.resize(wajah, (px, px), interpolation=ocv.INTER_LANCZOS4)
            return wajah
        return []

    def training_lbph(self, citra, label):
        lbph = ocv.face.LBPHFaceRecognizer_create()
        lbph.train(citra, label)
        lbph.write(self.classifier_path)

    def recognize_lbph(self, citra):
        # kenali wajah menggunakan metode LBPH
        self.classifier.read(self.classifier_path)
        return self.classifier.predict(citra)

    def recognize_citra(self, citra):
        citra = Image.open(citra)
        # kenali wajah dari citra yg diberikan
        citra = self.prepare_image(citra)
        return self.recognize_lbph(np.asarray(citra, "uint8"))

    def confidence2percent(self, confidence):
        percent_num = round(100 - confidence)
        percent = "{0}%".format(round(100 - confidence))

        return percent_num, percent
