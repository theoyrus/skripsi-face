from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CitrawajahModelPermissions(permissions.DjangoModelPermissions):
    # Atur permission untuk data citrawajah sesuai hak akses group & action
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS and view.action == "list":
            return True  # dihandle by queryset
        else:
            if view.action == "create":
                # POST create
                return request.user.has_perm("facerecog.add_citrawajah")
            elif view.action == "retrieve":
                # GET detail
                return (
                    request.user.user_karyawan.karyawan_id
                    == view.get_object().karyawan_id
                    or request.user.has_perm("facerecog.view_another_citrawajah")
                )
            elif view.action in ["update", "partial_update"]:
                # PUT/PATCH detail
                return (
                    request.user.user_karyawan.karyawan_id
                    == view.get_object().karyawan_id
                    or request.user.has_perm("facerecog.change_another_citrawajah")
                )
            elif view.action == "destroy":
                # DELETE detail
                return (
                    request.user.user_karyawan.karyawan_id
                    == view.get_object().karyawan_id
                    or request.user.has_perm("facerecog.delete_another_citrawajah")
                )
        return False
