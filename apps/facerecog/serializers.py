from rest_framework import serializers
from apps.facerecog.models import CitraWajah
from apps.karyawan.serializers import KaryawanMeSerializer
from apps.main.serializers import BaseHyperlinkedModelSerializer, BaseModelSerializer


class CitraWajahKaryawanSerializer(BaseHyperlinkedModelSerializer):
    # karyawan_nama = serializers.ReadOnlyField(source="karyawan.nama")
    # karyawan = KaryawanMeSerializer()

    class Meta:
        model = CitraWajah
        # fields = "__all__"
        fields = ("url", "citrawajah_id", "karyawan", "nama", "created", "updated")


MAX_IMAGE_SIZE = 2 * 1024 * 1024  # maksimum 2 MB
MAX_IMAGE_SIZE_MB = MAX_IMAGE_SIZE / 1024 / 1024


class CitraWajahUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitraWajah
        fields = ["karyawan", "nama"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get("request").user
        if user.has_perm("facerecog.add_another_citrawajah") or user.is_superuser:
            self.fields["karyawan"].required = True
        else:
            self.fields.pop("karyawan")

    def validate_nama(self, nama):
        if nama.size > MAX_IMAGE_SIZE:
            raise serializers.ValidationError(
                f"Ukuran citra terlalu besar, maksimal {MAX_IMAGE_SIZE_MB} MB"
            )
        return nama

    def validate(self, data):
        request = self.context["request"]
        user = request.user

        if user.has_perm("facerecog.add_another_citrawajah") or user.is_superuser:
            data["karyawan_id"] = self.initial_data["karyawan"]
        else:
            # jika tidak punya hak, maka kunci sesi karyawan
            data["karyawan_id"] = request.user.user_karyawan.karyawan_id

        return super().validate(data)


class CitraWajahRecognizeSerializer(serializers.Serializer):
    citra = serializers.ImageField()

    def validate_citra(self, citra):
        if citra.size > MAX_IMAGE_SIZE:
            raise serializers.ValidationError(
                f"Ukuran citra terlalu besar, maksimal {MAX_IMAGE_SIZE_MB} MB"
            )
        return citra
