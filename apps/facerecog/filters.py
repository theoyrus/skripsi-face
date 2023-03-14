from django_filters import rest_framework as filters


class CitraWajahFilter(filters.FilterSet):
    karyawan_id = filters.CharFilter(
        field_name="karyawan_id",
        lookup_expr="exact",
        help_text="Filter exact karyawan_id",
    )
