from rest_framework import serializers

from apps.authentication.serializers import UserSerializer
from apps.main.serializers import BaseHyperlinkedModelSerializer, BaseModelSerializer

from .models import Divisi, Karyawan, get_user_model

User = get_user_model()


class DivisiSerializer(BaseHyperlinkedModelSerializer):
    class Meta:
        model = Divisi
        fields = ("url", "divisi_id", "kode", "nama")


class DivisiCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Divisi
        fields = ("divisi_id", "kode", "nama")


class KaryawanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Karyawan
        fields = ("noinduk", "nama", "user", "divisi")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get("request").user
        if user.has_perm("karyawan.change_another_karyawan") or user.is_superuser:
            self.fields["user"].required = True
        else:
            self.fields.pop("user")

    def validate(self, data):
        request = self.context["request"]
        user = request.user

        if user.has_perm("karyawan.change_another_karyawan") or user.is_superuser:
            data["user_id"] = self.initial_data["user"]
        else:
            # jika tidak punya hak, maka kunci sesi karyawan
            data["user_id"] = request.user.user_id

        return super().validate(data)


class KaryawanMeUpdateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Karyawan
        fields = ("noinduk", "nama", "user", "divisi")


class KaryawanMeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # user_id = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(), required=True, write_only=True
    # )
    divisi = DivisiSerializer(read_only=True)
    # divisi_id = serializers.PrimaryKeyRelatedField(
    #     many=False, write_only=True, queryset=Divisi.objects.all()
    # )

    class Meta:
        model = Karyawan
        fields = ("noinduk", "nama", "user", "divisi")


class KaryawanSerializer(BaseModelSerializer):
    from facerecog.serializers import CitraWajahKaryawanSerializer

    user = serializers.StringRelatedField()
    user = UserSerializer(context={"is_data": False})
    divisi = DivisiSerializer(context={"is_data": False})
    citra_karyawan = CitraWajahKaryawanSerializer(many=True, read_only=True)

    class Meta:
        model = Karyawan
        fields = [
            "url",
            "karyawan_id",
            "noinduk",
            "nama",
            "user",
            "divisi",
            "citra_karyawan",
        ]
        # fields = "__all__"


class KaryawanCitraSerializer(serializers.ModelSerializer):

    from facerecog.serializers import CitraWajahKaryawanSerializer

    citra_wajah = CitraWajahKaryawanSerializer(many=True, read_only=True)

    user_link = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="user-detail"
    )

    class Meta:
        model = Karyawan
        fields = [
            "url",
            "karyawan_id",
            "noinduk",
            "nama",
            "user",
            "user_link",
            "citra_wajah",
        ]
        # fields = "__all__"
