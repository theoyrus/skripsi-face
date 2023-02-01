from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Custom Token Payloads
class AppTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # custom claims
        from django.core.exceptions import ObjectDoesNotExist

        token["user_id"] = user.id
        token["username"] = user.username
        try:
            kary = user.user_karyawan
            token["karyawan_id"] = kary.karyawan_id
            token["karyawan_nama"] = kary.nama
        except ObjectDoesNotExist:
            from core.helpers.exception_api import KaryawanUserError

            # raise KaryawanUserError("Sesi user karyawan belum diatur")
            token["karyawan_id"] = None
            token["karyawan_nama"] = None

        return token


class AppTokenObtainPairView(TokenObtainPairView):
    serializer_class = AppTokenObtainPairSerializer
