from django_filters import rest_framework as filters


class KehadiranFilter(filters.FilterSet):
    karyawan_id = filters.CharFilter(
        field_name="karyawan_id",
        lookup_expr="exact",
        help_text="Filter exact karyawan_id",
    )
    karyawan_nama = filters.CharFilter(
        field_name="karyawan__nama",
        lookup_expr="icontains",
        help_text="Filter contains karyawan.nama",
    )
    divisi_id = filters.CharFilter(
        field_name="karyawan__divisi_id",
        lookup_expr="exact",
        help_text="Filter exact divisi.id",
    )
    tahun = filters.NumberFilter(
        field_name="tanggal",
        lookup_expr="year",
        help_text="Filter tahun presensi",
    )
    bulan = filters.NumberFilter(
        field_name="tanggal",
        lookup_expr="month",
        help_text="Filter bulan presensi",
    )
