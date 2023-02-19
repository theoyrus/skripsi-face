from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions


class PresensiKehadiranPermission(permissions.DjangoModelPermissions):
    # Atur permission untuk data presensi sesuai hak akses group & action
    def has_permission(self, request, view):
        try:
            if request.method in permissions.SAFE_METHODS and view.action == "list":
                return True  # dihandle by queryset
            else:
                if view.action == "create":
                    # POST create
                    return request.user.has_perm("presensi.add_presensi")
                elif view.action == "retrieve":
                    # GET detail
                    return (
                        request.user.user_karyawan.karyawan_id
                        == view.get_object().karyawan_id
                        or request.user.has_perm("presensi.view_another_presensi")
                    )
                elif view.action in ["update", "partial_update"]:
                    # PUT/PATCH detail
                    return (
                        request.user.user_karyawan.karyawan_id
                        == view.get_object().karyawan_id
                        and request.user.has_perm("presensi.change_presensi")
                    ) or request.user.has_perm("presensi.change_another_presensi")
                elif view.action == "destroy":
                    # DELETE detail
                    return (
                        request.user.user_karyawan.karyawan_id
                        == view.get_object().karyawan_id
                        or request.user.has_perm("presensi.delete_another_presensi")
                    )
            return False
        except ObjectDoesNotExist:
            # jika user tidak punya relasi karyawan, tetap bisa asalkan superuser
            return request.user.is_superuser
