from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class KaryawanModelPermissions(permissions.DjangoModelPermissions):
    # Atur permission untuk data karyawan sesuai hak akses group & action
    def has_permission(self, request, view):
        try:
            if request.method in permissions.SAFE_METHODS and view.action == "list":
                return request.user.has_perm("karyawan.view_karyawan")
            else:
                if view.action == "create":
                    return request.user.has_perm("karyawan.add_karyawan")
                elif view.action == "retrieve":
                    return (
                        request.user.user_karyawan.karyawan_id
                        == view.get_object().karyawan_id
                        or request.user.has_perm("karyawan.view_another_karyawan")
                    )
                elif view.action in ["update", "partial_update"]:
                    return (
                        request.user.user_karyawan.karyawan_id
                        == view.get_object().karyawan_id
                        or request.user.has_perm("karyawan.change_another_karyawan")
                    )
                    return False
                elif view.action == "destroy":
                    return (
                        request.user.user_karyawan.karyawan_id
                        == view.get_object().karyawan_id
                        or request.user.has_perm("karyawan.delete_karyawan")
                    )
        except ObjectDoesNotExist:
            # jika user tidak punya relasi karyawan, tetap bisa asalkan superuser
            return request.user.is_superuser
