from django_filters import rest_framework as filters


class KaryawanFilter(filters.FilterSet):
    nama = filters.CharFilter(
        lookup_expr="icontains", help_text="Filter contains karyawan.nama"
    )
    divisi_nama = filters.CharFilter(
        field_name="divisi__nama",
        lookup_expr="icontains",
        help_text="Filter contains divisi.nama",
    )
